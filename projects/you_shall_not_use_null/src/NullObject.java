@Override
public List<Angel> findAll() {
    var angels = db.query(SQL_FIND_All);
    if (angels == null){
        return new List<Angel>();
    }
    return angels;
}