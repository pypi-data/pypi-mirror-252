from starlette_web.common.caches import caches
from starlette_web.tests.core.helpers.base_cache_tester import BaseCacheTester


class TestFileCache(BaseCacheTester):
    def test_file_cache_base_ops(self):
        self._run_base_cache_test(caches["files"])

    def test_file_cache_many_ops(self):
        self._run_cache_many_ops_test(caches["files"])

    def test_file_lock(self):
        self._run_cache_lock_test(caches["files"])

    def test_file_lock_race_condition(self):
        self._run_cache_mutual_lock_test(caches["files"])

    def test_file_lock_correct_task_blocking(self):
        self._run_locks_timeouts_test(caches["files"])

    def test_file_lock_cancellation(self):
        self._run_base_lock_cancellation(caches["files"])


class TestInMemoryCache(BaseCacheTester):
    def test_locmem_cache_base_ops(self):
        self._run_base_cache_test(caches["locmem"])

    def test_locmem_cache_many_ops(self):
        self._run_cache_many_ops_test(caches["locmem"])

    def test_locmem_lock(self):
        self._run_cache_lock_test(caches["locmem"])

    def test_locmem_lock_race_condition(self):
        self._run_cache_mutual_lock_test(caches["locmem"])

    def test_locmem_lock_correct_task_blocking(self):
        self._run_locks_timeouts_test(caches["locmem"])

    def test_file_lock_cancellation(self):
        self._run_base_lock_cancellation(caches["locmem"])
