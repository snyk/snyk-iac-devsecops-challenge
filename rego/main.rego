package main

allow[msg] {
    input.resource.local_file[name]
    msg := sprintf("resource.local_file.%s is allowed", [name])
}
