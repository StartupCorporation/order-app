from invoke.collection import Collection

from migrations import collection as migration_collection
from deps import collection as deps_collection


namespace = Collection()

namespace.add_collection(
    coll=migration_collection,
    name="migration",
)
namespace.add_collection(
    coll=deps_collection,
    name="deps",
)
