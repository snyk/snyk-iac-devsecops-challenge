package main

allow[msg] {
    input.resource.local_file[name]
    msg := sprintf("resource.local_file.%s is allowed", [name])
}

deny[msg] {
    module := input.module[name]
    startswith(module.source, "github.com")
    msg := sprintf("module.%s is not allowed", [name])
}
