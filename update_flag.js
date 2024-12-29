const dbName = process.env.DB_NAME;
const updatedBy = process.env.UPDATED_BY;
const target_machine = process.env.TARGET_MACHINE;

use(dbName);

const result = db.wol_info.updateOne(
  { _id: target_machine },
  {
    $set: {
      wol_switch: true,
      updated_time: new Date().toLocaleString("ja-JP", {
        timeZone: "Asia/Tokyo",
      }),
      updated_name: updatedBy,
    },
  },
  { upsert: true }
);

if (result.matchedCount > 0 || result.upsertedCount > 0) {
  print("Update successful.");
} else {
  print("Update failed.");
}
const updatedDocument = db.wol_info.findOne({ _id: target_machine });
print(updatedDocument);