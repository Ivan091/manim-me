@Override
public Angel findById(int id) {
    var map = db.query(SQL_FIND_BY_ID);
    if (map == null){
        return null;
    }
    return rowMapper.create(map);
}