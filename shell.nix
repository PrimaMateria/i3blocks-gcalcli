with import <nixpkgs> {};
let 
  pythonEnv = (python3.withPackages (ps: [
    ps.dateutil 
    ps.click
  ] ));
in mkShell {
  packages = [
    pythonEnv
    gcalcli
  ];
}
