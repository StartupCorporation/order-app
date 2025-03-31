from pathlib import Path

from dw_python_clis import ConfigVar, inner

from tasks.migrations import collection as migration_collection
from tasks.test_ import collection as test_collection


namespace = inner

namespace.add_collection(
    coll=migration_collection,
    name="migration",
)
namespace.add_collection(
    coll=test_collection,
    name="test",
)

namespace.configure(
    options={
        ConfigVar.ROOT_DIR: Path(__file__).parent.parent,
    },
)
