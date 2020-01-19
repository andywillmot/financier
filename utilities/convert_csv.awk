BEGIN {
    FPAT="([^,]*)|(\"([^\"]|(\"\"))*\")";
    AuthToken="<an auth token>";
    HostName="<ip address or hostname including protocol:\\ and :port>";
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

    print("curl -H \"Content-Type: application/json\" -H \"Authorization: Token " AuthToken "\" --request POST --data \x27" json "\x27 " HostName "/transactions/ && echo \"\"");
}
