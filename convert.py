#!/usr/bin/env python3
import sys
import json

content = {}
with open(sys.argv[1]) as file:
    content = json.load(file)

for run in content["runs"]:
    rdjson = {}
    tool = run["tool"]
    driver = tool["driver"]
    name = driver["name"]
    informationUri = driver["informationUri"]
    rule = {}
    ruleLevel = {}
    rdjson["source"] = {
        "name": name,
        "url": informationUri
    }
    diagnostics = []
    for r in driver["rules"]:
        id = r["id"]
        description = ""
        level = r["defaultConfiguration"]["level"]
        if level == "warning":
            level = "WARNING"
        elif level == "error":
            level = "ERROR"
        elif level == "note":
            level = "INFO"
        else:
            level = "UNKNOWN_SEVERITY"
        for item in ["shortDescription", "fullDescription", "help"]:
            if item in r:
                description += r[item]["text"] + "\n"
        rule[id] = description
        ruleLevel[id] = level
    for result in run["results"]:
        ruleId = result["ruleId"]
        description = rule[ruleId]
        # if "message" in result:
        #     description += result["message"]["text"] + "\n"
        sarifLocation = result["locations"][0]["physicalLocation"]
        path = sarifLocation["artifactLocation"]["uri"]
        location = {
            "path": path,
            "range": {
                "start": {
                    "line": sarifLocation["region"]["startLine"],
                    "column": sarifLocation["region"]["startColumn"]
                }
            }
        }
        if "endLine" in sarifLocation["region"]:
            location["range"]["end"] = {
                "line": sarifLocation["region"]["endLine"],
                "column": sarifLocation["region"]["endColumn"]
            }
        suggestions = []
        if "fixes" in result:
            for fix in result["fixes"]:
                ac = fix["artifactChanges"][0]
                if path != ac["artifactLocation"]["uri"]:
                    continue
                replace = ac["replacements"][0]
                deleted = replace["deletedRegion"]
                suggest = {
                    "range": {
                        "start": {
                            "line": deleted["startLine"],
                            "column": deleted["startColumn"]
                        },
                        "end": {
                            "line": deleted["endLine"],
                            "column": deleted["endColumn"]
                        }
                    }
                }
                if "insertedContent" in replace:
                    suggest["text"] = replace["insertedContent"]["text"]
                suggestions.append(suggest)
        diagnostic = {
            "message": description,
            "location": location,
            "severity": ruleLevel[ruleId],
            "code": {
                "value": ruleId,
            },
            "suggestions": suggestions,
        }
        diagnostics.append(diagnostic)
    rdjson["diagnostics"] = diagnostics
    print(json.dumps(rdjson))
