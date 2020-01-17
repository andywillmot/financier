BEGIN {
    FPAT="([^,]*)|(\"([^\"]|(\"\"))*\")";
}

{
    split($1,dt,"/")
    date = "\"" dt[3] "-" dt[2] "-" dt[1] "\"";
    order = "\""$2"\"";
    ttype = "\""$3"\""
    gsub(")","",ttype);
    account = "\""$4"\"";
    title = "\""$5"\"";
    gsub("\"","",title);
    gsub("\x27","",title);
    title = "\"" title "\""
    value = "\""$6"\"";

    json = "{\"date\": " date ", \"order\": " order ", \"ttype\": " ttype ", \"account\": " account ", \"title\": " title ", \"value\": " value "}";

    print("curl -H \"Content-Type: application/json\" -H \"Authorization: Token 0139ec908690345e0d7ae34417b2a4fd54b767b9\" --request POST --data \x27" json "\x27 http://localhost:8000/transactions/ && echo \"\"");
}
