"""
This module supports output handling
"""

import logging

from .output_handler import OutputHandler

logger = logging.getLogger(__name__)


class PlottingOutputHandler(OutputHandler):
    def on_after_infer(self, stage, predictions, metrics):
        super().on_after_infer(stage, predictions, metrics)

        self.visualize(predictions, stage)

    def visualize(self, predictions, dataloader_name):

        print(predictions)
        print(dataloader_name)

        """
        count = 1
        images, gts = self.dataloaders[dataloader_name][0]
        cols = len(images) // 3
        rows = len(images) // cols

        plt.figure(figsize=(12, 10))
        for idx, (im, gt, pred) in enumerate(zip(images, gts, predictions)):
            if idx == cols:
                break
            im = im.permute(0, 2, 1)
            gt = torch.amax(gt, dim=0)
            gt = gt.permute(1, 0)
            pred = pred.permute(1, 0)

            plot = Plot(is_multigpu=self.runtime_ctx.is_multigpu)

            count = plot.plot(cols, rows, count, im)
            count = plot.plot(cols, rows, count, im=gt, gt=True, title="Ground Truth")
            count = plot.plot(cols, rows, count, im=pred, title="Predicted Mask")
        plt.savefig(self.plot_output_path)
        """
