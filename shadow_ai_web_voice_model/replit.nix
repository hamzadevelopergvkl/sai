{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.requests
    pkgs.python310Packages.flask
  ];
}
