import argparse
import logging
import os
import os.path as osp
from datetime import datetime

from mmengine.config import Config, DictAction
from mmengine.logging import print_log
from mmengine.registry import RUNNERS
from mmengine.runner import Runner

from mmdet.utils import setup_cache_size_limit_of_dynamo

from geolibs.enginelogger_hook import EngineLoggerHook
from geolibs.engine_cocoext import EngineCocoExt
from geolibs.engine_mask import EngineMask
from geolibs.engine_csv import EngineCSV
from geolibs.engine_cocometric import EngineCocoMetric
from geolibs.loading import LoadBandsFromFile, LoadVariableSizedBandsFromFile, LoadMasks
from geolibs.transforms import ResizeAllToThisBand
from geolibs.misc import add_file_name_in_engine_tags, add_classes_to_package
from geolibs.engine_hub import weight_and_experiment


add_classes_to_package("mmengine.hooks",[EngineLoggerHook])
add_classes_to_package("mmdet.datasets",[EngineCocoExt])
add_classes_to_package("mmseg.datasets",[EngineMask])
add_classes_to_package("mmpretrain.datasets",[EngineCSV])
add_classes_to_package("mmcv.transforms",[LoadBandsFromFile,
                                          LoadVariableSizedBandsFromFile,
                                          ResizeAllToThisBand, LoadMasks])
add_classes_to_package("mmdet.evaluation.metrics",[EngineCocoMetric])


def parse_args():
    parser = argparse.ArgumentParser(description='Train a detector')
    parser.add_argument('config', help='train config file path')
    parser.add_argument('--work-dir', help='the dir to save logs and models')
    parser.add_argument(
        '--amp',
        action='store_true',
        default=False,
        help='enable automatic-mixed-precision training')
    parser.add_argument(
        '--auto-scale-lr',
        action='store_true',
        help='enable automatically scaling LR.')
    parser.add_argument(
        '--resume',
        nargs='?',
        type=str,
        help='If specify checkpoint path, resume from it, while if not '
        'specify, try to auto resume from the latest checkpoint '
        'in the work directory.')
    parser.add_argument(
        '--finetune',
        nargs='?',
        type=str,
        help='If specify checkpoint path, finetune from it.'
    )
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='job launcher')
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`.
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)

    return args


def main():
    args = parse_args()

    # Reduce the number of repeated compilations and improve
    # training speed.
    setup_cache_size_limit_of_dynamo()

    # load config
    cfg = Config.fromfile(args.config)
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    cfg = add_file_name_in_engine_tags(cfg)
    # work_dir is determined in this priority: CLI > segment in file > filename
    if args.work_dir is not None:
        # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs',
                                osp.splitext(osp.basename(args.config))[0])
    cfg.work_dir = f"{cfg.work_dir}-{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}"
    # enable automatic-mixed-precision training
    if args.amp is True:
        optim_wrapper = cfg.optim_wrapper.type
        if optim_wrapper == 'AmpOptimWrapper':
            print_log(
                'AMP training is already enabled in your config.',
                logger='current',
                level=logging.WARNING)
        else:
            assert optim_wrapper == 'OptimWrapper', (
                '`--amp` is only supported when the optimizer wrapper type is '
                f'`OptimWrapper` but got {optim_wrapper}.')
            cfg.optim_wrapper.type = 'AmpOptimWrapper'
            cfg.optim_wrapper.loss_scale = 'dynamic'

    # enable automatically scaling LR
    if args.auto_scale_lr:
        if 'auto_scale_lr' in cfg and \
                'enable' in cfg.auto_scale_lr and \
                'base_batch_size' in cfg.auto_scale_lr:
            cfg.auto_scale_lr.enable = True
        else:
            raise RuntimeError('Can not find "auto_scale_lr" or '
                               '"auto_scale_lr.enable" or '
                               '"auto_scale_lr.base_batch_size" in your'
                               ' configuration file.')

    # resume is determined in this priority: resume from > auto_resume
    if args.resume:
        cfg.resume = True
        if 'engine.granular.ai' in args.resume:
            dst_path, experiment_id = weight_and_experiment(args.resume)
            cfg.load_from = dst_path
            cfg.experiment_id = experiment_id
        else:
            cfg.load_from = args.resume
            cfg.experiment_id = None
    elif args.finetune:
        if 'engine.granular.ai' in args.finetune:
            dst_path, experiment_id = weight_and_experiment(args.finetune, best=True)
            cfg.load_from = dst_path
            cfg.experiment_id = experiment_id
        else:
            cfg.load_from = args.resume
            cfg.experiment_id = None
    else:
        cfg.experiment_id = None
        

    # build the runner from config
    if 'runner_type' not in cfg:
        # build the default runner
        runner = Runner.from_cfg(cfg)
    else:
        # build customized runner from the registry
        # if 'runner_type' is set in the cfg
        runner = RUNNERS.build(cfg)

    # start training
    runner.train()


if __name__ == '__main__':
    main()