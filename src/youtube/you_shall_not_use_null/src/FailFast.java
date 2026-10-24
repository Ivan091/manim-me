@Override
public Angel findById(int id) throws NotFoundException{
    var map = db.query(SQL_FIND_BY_ID);
    if (map == null){
        throw new NotFoundException("Angel wasn't found.")
    }
    return rowMapper.create(map);
}