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
    # If informationUri is not set, use a blank string
    informationUri = driver["informationUri"] if "informationUri" in driver else ""
    rule = {}
    ruleLevel = {}
    rdjson["source"] = {
        "name": name,
        "url": informationUri
    }
    diagnostics = []
    # if no rules, we can't do anything, so go to the next run
    if "rules" not in driver:
        continue
    for r in driver["rules"]:
        id = r["id"]
        description = "\n#### " + id + " "
        level = "warning"
        if level == "warning":
            level = "WARNING"
        elif level == "error":
            level = "ERROR"
        elif level == "note":
            level = "INFO"
        else:
            level = "UNKNOWN_SEVERITY"
        if "shortDescription" in r:
            description += r["shortDescription"]["text"] + ":\n"
        if "fullDescription" in r:
            description += r["fullDescription"]["text"] + "\n\n"
        if "help" in r:
            description += "*" + r["help"]["text"] + "*\n"
        rule[id] = description
        ruleLevel[id] = level
    for result in run["results"]:
        ruleId = result["ruleId"]
        description = rule[ruleId]
        # if "message" in result:
        #     description += result["message"]["text"] + "\n"
        sarifLocation = result["locations"][0]["physicalLocation"]
        path = sarifLocation["artifactLocation"]["uri"]
        # If there's no range, we can't do anything. Go to the next result
        if "region" not in sarifLocation:
            continue
        location = {
            "path": path,
            "range": {
                "start": {
                    "line": sarifLocation["region"]["startLine"],
                    "column": sarifLocation["region"]["startColumn"] if "startColumn" in sarifLocation["region"] else 1
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
                location["range"] = suggest["range"]
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
