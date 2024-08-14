import logging

from .metrics_cache import MetricsCache

logger = logging.getLogger(__name__)


class StoppingCriterion:
    def __init__(self):
        pass

    def on_result(self, _: MetricsCache) -> tuple[bool, bool]:
        return False, False


class NonDeacreasingEarlyStoppingCriterion(StoppingCriterion):
    """
    This class decides when a model training run should stop
    """

    def __init__(self, threshold: int = 7):
        super().__init__()
        self.threshold = threshold
        self.best_result: float = -1.0
        self.decreasing_count: int = 1
        self.num_epochs_without_improvement: int = 0

    def on_result(self, metrics_cache: MetricsCache) -> tuple[bool, bool]:
        """
        Given a result, decide whether to save the model and/or stop
        further computation
        """

        should_save_model = False
        should_finish_run = False

        result = metrics_cache.stage_results["loss"]

        if result < self.best_result:
            logger.info("Loss decreased from %0.3f to %0.3f", self.best_result, result)
            self.decreasing_count += 1
            if self.decreasing_count % 2 == 0:
                should_save_model = True
        elif result > self.best_result:
            self.num_epochs_without_improvement += 1
            logger.info(
                "Loss did not decrease for %s epoch(s)",
                self.num_epochs_without_improvement,
            )
            if self.num_epochs_without_improvement == self.threshold:
                logger.info("Stopping training as loss didn't decrease")
                should_finish_run = True
        self.best_result = result
        return should_save_model, should_finish_run
