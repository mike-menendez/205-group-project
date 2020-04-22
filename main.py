from fastapi import FastAPI, Response, status, Form
import os, datetime

app = FastAPI()

# Define a list of the available images to select the appropriate runtime
# Key: language tag -> tuple(image name, compile + execute command)
IMG_LIST = {
    "cpp": ("mmenendez/interviewhigh-cpp:ubuntu","cp ", " main.cpp; g++ -w -o main main.cpp 2> ", "err.out && for i in $(seq 1 $(cat input",
            " | wc -l)); do sed \"${i}q;d\" < input", " > $i && ./main < $i >> ", " && echo \"\nline\" >> "),
    "java": ("java", "javac"),
    "py": ("python3", "for i in $(cat input); do python3 main.py <0 $i 1>> out.txt 2> err.txt; done"),
    "js": ("node", "for i in $(cat input); do node app.js <$i 1>> out.txt 2> err.txt; done")
}

@app.get("/health", status_code=200)
async def health_check():
    return

@app.post("/eterm", status_code=200)
async def eterm(uuid: str = Form(...), lang: str = Form(...)):
    os.system(f"docker stop {uuid}{lang}")
    os.system(f"docker rm -f {uuid}{lang}")
    await clean_up({"uuid" : uuid})
    return "we gucci"

async def parse_res(params):
    if os.stat(params["uuid"] + "err.out").st_size != 0:
        for x in [params['uuid'], f"input{params['uuid']}", f"{params['uuid']}err.out"]: os.remove(x)
        return {"c_err": ["compilation error"]}
    f, ans, s = open(params["uuid"] + ".out", "r"), [], ""
    line = f.readline()
    while line:
        if line != "" and line != "line\n":
            s = s + line
        elif line == "line\n":
            ans.append(s.strip())
            s = ""
        line = f.readline()
    await clean_up(params)
    return {"results" : ans}

# Delete created files from user
async def clean_up(params):
    listy = [params["uuid"], f"input{params['uuid']}", f"{params['uuid']}.out", f"{params['uuid']}err.out"]
    for x in listy: os.remove(x)
    return

# Creates the files: user code and test cases
async def create_usr_files(params):
    usr = open(params["uuid"], mode="w")
    usr.write(params["code"])
    usr.close()
    if params["input"][len(params["input"]) -1] != "\n":
        params["input"] = params["input"] + "\n"
    test = open("input" + params["uuid"], mode="w")
    test.write(params["input"])
    test.close()
    return

async def runtime_service(params):
    await create_usr_files(params)
    cmd = []
    # create the container
    cmd.append("docker run -it -d --name=" + params["uuid"] + params["lang"] + " " + IMG_LIST[params["lang"]][0])
    # transfer code into container
    cmd.append("docker cp " + params["uuid"] + " " + params["uuid"] + params["lang"] + ":.")
    # transfer input into container
    cmd.append(f"docker cp input{params['uuid']} {params['uuid']}{params['lang']}:.")
    # execute command
    cmd.append("docker exec " + params["uuid"] + params["lang"] + " /bin/sh -c '" + 
            IMG_LIST[params["lang"]][1] + params["uuid"] + IMG_LIST[params["lang"]][2] + params["uuid"] +
            IMG_LIST[params["lang"]][3] + params["uuid"] + IMG_LIST[params["lang"]][4] + params["uuid"] +
            IMG_LIST[params["lang"]][5] + params["uuid"] +".out" + IMG_LIST[params["lang"]][6] + params["uuid"] + ".out; done'")
    # extract results
    cmd.append("docker cp " + params["uuid"] + params["lang"] + ":./" + params["uuid"] + ".out .; docker cp " +
            params["uuid"] + params["lang"] + ":./" + params["uuid"] + "err.out .")
    # stop and delete container
    cmd.append("docker stop " + params["uuid"] + params["lang"] + " && docker rm " + params["uuid"] + params["lang"])
    for x in cmd: os.system(f"{x} > /dev/null 1>&2")
    return await parse_res(params)

# Driver code for the rts endpoint
@app.post("/", status_code=200)
async def rts(*, uuid: str = Form(...), input: str = Form(...), code: str = Form(...),
            question_id: str = Form(...), lang: str = Form(...), response: Response):
    results = await runtime_service({ "uuid" : uuid, "input" : input, "code" : code, "question_id" : question_id, "lang" : lang })
    if "c_err" in results.keys(): response.status_code = 400
    return results