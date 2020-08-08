"""
Usage: arangoimp [<options>]

Section 'global options' (Global configuration)
  --backslash-escape <boolean>           使用反斜线作为转意字符(default: false)
  --batch-size <uint64>                  每次数据量大小 (in bytes) (default: 16777216)
  --collection <string>                  要导入的集合名字 (default: "")
  --create-collection <boolean>          当集合不存在时创建集合 (default: false)
  --create-collection-type <string>      创建集合类型 (edge or document).(default:  "document")
  --file <string>                        导入文件名
  --from-collection-prefix <string>      _from 集合名前缀
  --overwrite <boolean>                  当集合已经存在时覆盖集合(default: false)
  --separator <string>                   字段分隔符,csv或tsv使用(default: "")
  --to-collection-prefix <string>        _to 集合名前缀
  --type <string>                        导入文件类型. possible values: "auto", "csv", "json", "jsonl", "tsv" (default: "json")

Section 'server' (Configure a connection to the server)
  --server.connection-timeout <double>   连接超时时间(default: 5)
  --server.database <string>             连接数据库名(default: "_system")
  --server.password <string>             连接密码. 如果没有特殊指定，需要使用密码，用户将被提醒索要一份密码(default: "")
  --server.request-timeout <double>      访问超时时间（秒） (default:1200)
  --server.username <string>             连接时用户名(default: "root")
  --server.endpoint                      endpoint to connect to, use 'none' to start without a server (default: "http+tcp://127.0.0.1:8529")
"""
from subprocess import Popen, DEVNULL

sh = "arangoimp --batch-size 100000000 --collection {collection_name} --create-collection true " \
     "--create-collection-type {type} --file {file} --overwrite true --type json " \
     "--server.database {db} --server.username {user} --server.password {passwd} --server.endpoint {addr}"

# entity
entity_cmd = sh.format(collection_name="tripitaka_entity", type="document",
                       file="./results/tripitaka_entity.json",
                       db="_system", user="root", passwd="rai", addr="tcp://127.0.0.1:8529")

# relation
relation_cmd = sh.format(collection_name="tripitaka_relation", type="edge",
                         file="./results/tripitaka_relation.json",
                         db="_system", user="root", passwd="rai", addr="tcp://127.0.0.1:8529") + \
               " --from-collection-prefix tripitaka_entity --to-collection-prefix tripitaka_entity"

with Popen(entity_cmd, shell=True, stdout=DEVNULL) as e:
    print(entity_cmd)
    print(e.returncode)

with Popen(relation_cmd, shell=True, stdout=DEVNULL) as r:
    print(relation_cmd)
    print(r.returncode)
