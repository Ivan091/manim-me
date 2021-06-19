collection.forEach(x -> {
    if (x != null){
        x.doStuff();
    } else {
        doSomethingElse();
    }
})