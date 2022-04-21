const sqlite = require('sqlite3').verbose();
let db = new sqlite.DATABASE('tracker.db',(err)=>{
    if (err){
        return console.log(err.message)
    }else{
        console.log('Successfully connected')

    }
})

