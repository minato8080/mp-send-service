const dbName = process.env.DB_NAME;
const updatedBy = process.env.UPDATED_BY;
const target_machine = process.env.TARGET_MACHINE;

use(dbName);

const updatedDocument = db.wol_info.findOne({ _id: target_machine });
print(updatedDocument);