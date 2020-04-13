from aiohttp import web
import uvloop, asyncio, os, logging, datetime

# Define a list of the available images to select the appropriate runtime
# Key: language tag -> tuple(image name, compile + execute command)
IMG_LIST = {
    "cpp": ("mmenendez/interviewhigh-cpp:ubuntu","cp ", " main.cpp; g++ -w -o main main.cpp 2> ", "err.out && for i in $(seq 1 $(cat input",
            " | wc -l)); do sed \"${i}q;d\" < input", " > $i && ./main < $i >> ", " && echo \"\nline\" >> "),
    "java": ("java", "javac"),
    "py": ("python3", "for i in $(cat input); do python3 main.py <0 $i 1>> out.txt 2> err.txt; done"),
    "js": ("node", "for i in $(cat input); do node app.js <$i 1>> out.txt 2> err.txt; done")
}

# Initalizes the logger, aiohttp server, declare routes, uvloop, runs server
def main():
    logging.basicConfig(filename="err.log", level=(os.getenv("LOG_LEVEL") or "ERROR"))
    try:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except BaseException:
        logging.error("Failed to set uvloop binding, using default")
    app = web.Application()
    app.add_routes([web.post("/", rts), web.get("/health", health_check), web.post("/eterm", early_term)])
    web.run_app(app, port=80)

def health_check(request):
    return web.Response(status=200)

async def early_term(request):
    try:
        data = await request.post()
        params, required = {}, ["uuid", "lang"]
        for k in required:
            if data.get(k) is None:
                raise KeyError(f"Could not find {k} in POST data")
            else:
                params[k] = data.get(k)
    except BaseException as e:
        logging.error(["Invalid request format", e])
        return web.Response(status=400)
    os.system("docker kill " + params["uuid"] + params["lang"] + "; docker rm --force " + params["uuid"] + params["lang"] + " > /dev/null 1>&2")
    await clean_up(params)
    return web.Response(status=200)

async def parse_res(params):
    if os.stat(params["uuid"] + "err.out").st_size != 0:
        os.remove(params["uuid"])
        os.remove("input" + params["uuid"])
        os.remove(params["uuid"] + "err.out")
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
    os.remove(params["uuid"])
    os.remove("input" + params["uuid"])
    os.remove(params["uuid"] + ".out")
    os.remove(params["uuid"] + "err.out")
    return

# Auxilary function, creates the files: user code and test cases, then bundles into a tar archive
async def create_usr_files(params):
    usr = open(params["uuid"], mode="w")
    usr.write(params["code"])
    usr.close()
    os.chmod(params["uuid"], 0o777)
    if params["input"][len(params["input"]) -1] != "\n":
        params["input"] = params["input"] + "\n"
    test = open("input" + params["uuid"], mode="w")
    test.write(params["input"])
    test.close()
    os.chmod("input" + params["uuid"], 0o777)
    return

async def runtime_service(params):
    cmd = []
    await create_usr_files(params)
    # create the container
    cmd.append("docker run -it -d --name=" + params["uuid"] + params["lang"] + " " + IMG_LIST[params["lang"]][0])
    # transfer code into container
    cmd.append("docker cp " + params["uuid"] + " " + params["uuid"] + params["lang"] + ":.")
    # transfer input into container
    cmd.append("docker cp input" + params["uuid"] + " " + params["uuid"] + params["lang"] + ":.")
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

    for x in cmd: os.system(x + " > /dev/null 1>&2")
    result = await parse_res(params)
    return result

# Driver code for the rts endpoint
async def rts(request):
    try:
        data = await request.post()
        params, required = {}, ["uuid", "code", "input", "question_id", "lang"]
        for k in required:
            if data.get(k) is None:
                raise KeyError(f"Could not find {k} in POST data")
            else:
                params[k] = data.get(k)
    except BaseException as e:
        logging.error(msg="Invalid request format")
        logging.error(e)
        return web.Response(status=400)
    return web.json_response(status=200, data= await runtime_service(params))

if __name__ == "__main__":
    main()
