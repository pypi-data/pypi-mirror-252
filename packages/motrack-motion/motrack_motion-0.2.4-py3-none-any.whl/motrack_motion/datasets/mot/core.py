"""
MOT Challenge Dataset support
"""
import configparser
import copy
import enum
import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List, Any, Union, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

from motrack_motion.datasets.common.scene_info import BasicSceneInfo
from motrack_motion.datasets.torch import TrajectoryDataset
from motrack_motion.datasets.utils import split_trajectory_observed_unobserved
from motrack_motion.utils import file_system

CATEGORY = 'pedestrian'
SEPARATOR = '+'
N_IMG_DIGITS = 6

class LabelType(enum.Enum):
    DETECTION = 'det'
    GROUND_TRUTH = 'gt'


@dataclass
class SceneInfo(BasicSceneInfo):
    """
    MOT Scene metadata (name, frame shape, ...)
    """
    dirpath: str
    gt_path: str
    framerate: Union[str, int]
    imdir: str
    imext: str

    def __post_init__(self):
        """
        Convert to proper type
        """
        super().__post_init__()
        self.framerate = int(self.framerate)


SceneInfoIndex = Dict[str, SceneInfo]


logger = logging.getLogger('MOTDataset')


class MOTDataset(TrajectoryDataset):
    """
    Parses MOT dataset in given format
    """
    def __init__(
        self,
        paths: Union[str, List[str]],
        history_len: int,
        future_len: int,
        sequence_list: Optional[List[str]] = None,
        label_type: LabelType = LabelType.GROUND_TRUTH,
        skip_corrupted: bool = False,
        test: bool = False
    ) -> None:
        """
        Args:
            paths: One more dataset paths
            history_len: Number of observed data points
            future_len: Number of unobserved data points
            sequence_list: Sequence filter by defined list
            label_type: Label Type
            skip_corrupted: Skip corrupted scenes (otherwise error is raised)
            test: Is this dataset used for test evaluation
        """
        super().__init__(
            history_len=history_len,
            future_len=future_len,
            sequence_list=sequence_list
        )

        if isinstance(paths, str):
            paths = [paths]

        self._label_type = label_type
        self._scene_info_index, self._n_digits = self._index_dataset(paths, label_type, sequence_list, skip_corrupted, test=test)
        self._data_labels, self._n_labels, self._frame_to_data_index_lookup = self._parse_labels(self._scene_info_index, test=test)
        self._trajectory_index = self._create_trajectory_index(self._data_labels, self._history_len, self._future_len, test=test)

    @property
    def label_type(self) -> LabelType:
        """
        Returns: LabelType
        """
        return self._label_type

    @property
    def scenes(self) -> List[str]:
        return list(self._scene_info_index.keys())

    def parse_object_id(self, object_id: str) -> Tuple[str, str]:
        assert object_id in self._data_labels, f'Unknown object id "{object_id}".'
        scene_name, scene_object_id = object_id.split(SEPARATOR)
        return scene_name, scene_object_id

    def get_object_category(self, object_id: str) -> str:
        return CATEGORY

    def get_scene_object_ids(self, scene_name: str) -> List[str]:
        assert scene_name in self.scenes, f'Unknown scene "{scene_name}". Dataset scenes: {self.scenes}.'
        return [d for d in self._data_labels if d.startswith(scene_name)]

    def get_scene_number_of_object_ids(self, scene_name: str) -> int:
        return len(self.get_scene_object_ids(scene_name))

    def get_object_data_length(self, object_id: str) -> int:
        return len(self._data_labels[object_id])

    def get_object_data_label(self, object_id: str, index: int, relative_bbox_coords: bool = True) -> Optional[dict]:
        data = copy.deepcopy(self._data_labels[object_id][index])
        if data is None:
            return data

        if relative_bbox_coords:
            scene_name, _ = self.parse_object_id(object_id)
            scene_info = self._scene_info_index[scene_name]
            bbox = data['bbox']
            bbox = [
                bbox[0] / scene_info.imwidth,
                bbox[1] / scene_info.imheight,
                bbox[2] / scene_info.imwidth,
                bbox[3] / scene_info.imheight
            ]
            data['bbox'] = bbox

        return data

    def get_object_data_label_by_frame_index(
        self,
        object_id: str,
        frame_index: int,
        relative_bbox_coords: bool = True
    ) -> Optional[dict]:
        return self.get_object_data_label(object_id, frame_index, relative_bbox_coords=relative_bbox_coords)

    def get_scene_info(self, scene_name: str) -> BasicSceneInfo:
        return self._scene_info_index[scene_name]

    def _get_image_path(self, scene_info: SceneInfo, frame_id: int) -> str:
        """
        Get frame path for given scene and frame id

        Args:
            scene_info: scene metadata
            frame_id: frame number

        Returns:
            Path to image (frame)
        """
        return os.path.join(scene_info.dirpath, scene_info.imdir, f'{frame_id:0{self._n_digits}d}{scene_info.imext}')

    def get_scene_image_path(self, scene_name: str, frame_index: int) -> str:
        scene_info = self._scene_info_index[scene_name]
        return self._get_image_path(scene_info, frame_index + 1)

    @staticmethod
    def _get_data_cache_path(path: str, data_name: str) -> str:
        """
        Get cache path for data object path.

        Args:
            path: Path

        Returns:
            Path where data object is or will be stored.
        """
        filename = Path(path).stem
        cache_filename = f'.{filename}.{data_name}.json'
        dirpath = str(Path(path).parent)
        return os.path.join(dirpath, cache_filename)

    @staticmethod
    def parse_scene_ini_file(scene_directory: str, label_type_name) -> SceneInfo:
        gt_path = os.path.join(scene_directory, label_type_name, f'{label_type_name}.txt')
        scene_info_path = os.path.join(scene_directory, 'seqinfo.ini')
        raw_info = configparser.ConfigParser()
        raw_info.read(scene_info_path)
        raw_info = dict(raw_info['Sequence'])
        raw_info['gt_path'] = gt_path
        raw_info['dirpath'] = scene_directory

        return SceneInfo(**raw_info, category=CATEGORY)

    @staticmethod
    def _index_dataset(
        paths: List[str],
        label_type: LabelType,
        sequence_list: Optional[List[str]],
        skip_corrupted: bool,
        test: bool = False
    ) -> Tuple[SceneInfoIndex, int]:
        """
        Index dataset content. Format: { {scene_name}: {scene_labels_path} }

        Args:
            paths: Dataset paths
            label_type: Use ground truth bboxes or detections
            sequence_list: Filter scenes
            skip_corrupted: Skips incomplete scenes
            test: Is it test split

        Returns:
            Index to scenes, number of digits used in images name convention (may vary between datasets)
        """
        n_digits = N_IMG_DIGITS
        scene_info_index: SceneInfoIndex = {}

        for path in paths:
            scene_names = [file for file in file_system.listdir(path) if not file.startswith('.')]
            logger.debug(f'Found {len(scene_names)} scenes for dataset "{path}". Names: {scene_names}.')

            n_skipped: int = 0

            for scene_name in scene_names:
                if sequence_list is not None and scene_name not in sequence_list:
                    continue

                scene_directory = os.path.join(path, scene_name)
                scene_files = file_system.listdir(scene_directory)

                # Scene content validation
                skip_scene = False
                for filename in [label_type.value, 'seqinfo.ini']:
                    if filename not in scene_files:
                        if filename == label_type.value and test:
                            continue

                        msg = f'Ground truth file "{filename}" not found on path "{scene_directory}". Contents: {scene_files}'
                        if not skip_corrupted:
                            raise FileNotFoundError(msg)

                        logger.warning(f'Skipping scene "{scene_name}" for dataset "{path}". Reason: `{msg}`')
                        skip_scene = True
                        break

                if 'img1' in scene_files:
                    # Check number of digits used in image name (e.g. DanceTrack and MOT20 have different convention)
                    img1_path = os.path.join(scene_directory, 'img1')
                    image_names = file_system.listdir(img1_path)
                    assert len(image_names) > 0, f'Image folder exists but it is empty! Dataset: "{path}"'
                    image_name = Path(image_names[0]).stem
                    n_digits = len(image_name)

                if skip_scene:
                    n_skipped += 1
                    continue

                scene_info = MOTDataset.parse_scene_ini_file(scene_directory, label_type.value)
                scene_info_index[scene_name] = scene_info
                logger.debug(f'Scene info {scene_info}.')

            if n_digits != N_IMG_DIGITS:
                logger.warning(f'Dataset "{path}" does not have default number of digits in image name. '
                               f'Got {n_digits} where default is {N_IMG_DIGITS}.')

            logger.info(f'Total number of parsed scenes is {len(scene_info_index)}. '
                        f'Number of skipped scenes is {n_skipped} for path "{path}".')

        return scene_info_index, n_digits

    def _parse_labels(self, scene_infos: SceneInfoIndex, test: bool = False) -> Tuple[Dict[str, List[dict]], int, Dict[str, Dict[int, int]]]:
        """
        Loads all labels dictionary with format:
        {
            {scene_name}_{object_id}: {
                {frame_id}: [ymin, xmin, w, h]
            }
        }

        Args:
            scene_infos: Scene Metadata
            test: If test then no parsing is performed

        Returns:
            Labels dictionary
        """
        data: Dict[str, List[Optional[dict]]] = {}
        frame_to_data_index_lookup: Dict[str, Dict[int, int]] = defaultdict(dict)
        n_labels = 0
        if test:
            # Return empty labels
            return data, n_labels, frame_to_data_index_lookup

        for scene_name, scene_info in scene_infos.items():
            seqlength = self._scene_info_index[scene_name].seqlength

            df = pd.read_csv(scene_info.gt_path, header=None)
            df = df[df[7] == 1]  # Ignoring values that are not evaluated

            df = df.iloc[:, :6]
            df.columns = ['frame_id', 'object_id', 'xmin', 'ymin', 'w', 'h']  # format: yxwh
            df['object_global_id'] = \
                scene_name + SEPARATOR + df['object_id'].astype(str)  # object id is not unique over all scenes
            df = df.drop(columns='object_id', axis=1)
            df = df.sort_values(by=['object_global_id', 'frame_id'])
            n_labels += df.shape[0]

            object_groups = df.groupby('object_global_id')
            for object_global_id, df_grp in tqdm(object_groups, desc=f'Parsing {scene_name}', unit='pedestrian'):
                df_grp = df_grp.drop(columns='object_global_id', axis=1).set_index('frame_id')

                data[object_global_id] = [None for _ in range(seqlength)]
                for frame_id, row in df_grp.iterrows():
                    data[object_global_id][int(frame_id) - 1] = {
                        'frame_id': frame_id,
                        'bbox': row.values.tolist(),
                        'image_path': self._get_image_path(scene_info, frame_id),
                        'occ': False,
                        'oov': False,
                        'scene': scene_name,
                        'category': CATEGORY
                    }
                    frame_to_data_index_lookup[object_global_id][frame_id] = len(data[object_global_id]) - 1

        logger.debug(f'Parsed labels. Dataset size is {n_labels}.')
        data = dict(data)  # Disposing unwanted defaultdict side-effects
        return data, n_labels, frame_to_data_index_lookup

    def _create_trajectory_index(
        self,
        labels: Dict[str, List[Optional[dict]]],
        history_len: int,
        future_len: int,
        test: bool = False
    ) -> List[Tuple[str, int, int]]:
        """
        Creates trajectory index by going through every object and creating bbox trajectory of consecutive time points.
        All trajectories that are not continuous are skipped.

        Args:
            labels: List of bboxes for each object
            history_len: Length of observed part of trajectory
            future_len: Length of unobserved part of trajectory
            test: If test then no parsing is performed

        Returns:
            Trajectory index
        """
        trajectory_len = history_len + future_len
        traj_index = []

        if test:
            return traj_index

        # Skipped trajectories stats
        n_skipped = 0
        n_total = 0

        for object_global_id, data in tqdm(labels.items(), desc='Creating trajectories', unit='object'):
            # Fetch scene length
            scene_name, _ = self.parse_object_id(object_global_id)
            seqlength = self._scene_info_index[scene_name].seqlength

            # Add trajectories to the index
            traj_start_time_point_candidates = list(range(seqlength))
            for i in traj_start_time_point_candidates:
                if i + trajectory_len > seqlength:  # Out of range
                    continue

                n_total += 1

                trajectory_range = list(range(i, i + trajectory_len))
                if any((data[frame_id] is None) for frame_id in trajectory_range):
                    # Trajectory is not continuous -> skipping
                    # Note: This is only for motion model training
                    n_skipped += 1
                    continue

                traj_index.append((object_global_id, i, i + trajectory_len))

        n_kept = n_total - n_skipped
        logger.info(f'Total number of trajectory candidates: {n_total}.')
        logger.info(f'Total number of skipped trajectories: {n_skipped} (ratio: {100 * (n_skipped / n_total):.2f}%).')
        logger.info(f'Total number of kept trajectories: {n_kept}.')
        logger.info(f'Trajectory index size: {len(traj_index)}')

        return traj_index

    def __len__(self) -> int:
        return len(self._trajectory_index)

    def __getitem__(self, index: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
        object_id, traj_start, traj_end = self._trajectory_index[index]
        raw_traj = self._data_labels[object_id][traj_start:traj_end]
        traj_len = len(raw_traj)
        expected_traj_len = self._history_len + self._future_len
        assert traj_len == self._history_len + self._future_len, f'Expected length {expected_traj_len} but got {traj_len}!'

        scene_name = object_id.split(SEPARATOR)[0]
        scene_info = self._scene_info_index[scene_name]

        # Metadata
        frame_ids = [item['frame_id'] for item in raw_traj]
        metadata = {
            'category': CATEGORY,
            'scene_name': scene_name,
            'object_id': object_id,
            'frame_ids': frame_ids,
            'image_paths': [item['image_path'] for item in raw_traj]
        }

        # Bboxes
        bboxes = np.array([item['bbox'] for item in raw_traj], dtype=np.float32)
        # Normalize bbox coordinates
        bboxes[:, [0, 2]] /= scene_info.imwidth
        bboxes[:, [1, 3]] /= scene_info.imheight

        bboxes_obs, bboxes_unobs, frame_ts_obs, frame_ts_unobs = \
            split_trajectory_observed_unobserved(frame_ids, bboxes, self._history_len)
        return bboxes_obs, bboxes_unobs, frame_ts_obs, frame_ts_unobs, metadata
