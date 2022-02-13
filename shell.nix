with import <nixpkgs> {};
let 
  pythonEnv = (python3.withPackages (ps: [ ] ));
in mkShell {
  packages = [
    pythonEnv
  ];
}
