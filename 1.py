f=input()
with open(f,"r",encoding='utf-8') as file:
    content=file.read().replace("\t","")
with open(f,"w",encoding='utf-8') as file:
    foo=content.replace("\n\n","\n")
    while(foo!=content):
        content=foo
        foo=content.replace("\n\n","\n")
    file.write(foo)