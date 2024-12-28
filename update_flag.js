const dbName = process.env.DB_NAME;
const updatedBy = process.env.UPDATED_BY;

use(dbName);

const result = db.wol_info.updateOne(
    { "key": "target_flag" },
    { $set: { "bool_value": true, "updated_at": new Date(), "updated_by": updatedBy } },
    { upsert: true }
);

if (result.matchedCount > 0) {
    print("更新が成功しました。");
} else {
    print("更新に失敗しました。");
}