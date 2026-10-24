@Override
public Optional<Angel> findById(int id) {
    var map = db.query(SQL_FIND_BY_ID);
    if (map == null){
        return Optional.empty();
    }
    return Optional.of(rowMapper.create(map));
}