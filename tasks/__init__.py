from invoke.collection import Collection

from tasks.deps import collection as deps_collection
from tasks.migrations import collection as migration_collection
from tasks.test_ import collection as test_collection

namespace = Collection()

namespace.add_collection(
    coll=migration_collection,
    name="migration",
)
namespace.add_collection(
    coll=deps_collection,
    name="deps",
)
namespace.add_collection(
    coll=test_collection,
    name="test",
)
