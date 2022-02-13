{
  description = "Shows upcoming event in the status bar and full month when clicked on.";
  inputs.nixpkgs.url = "nixpkgs/nixos-21.11";
  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.i3blocks-gcalcli = 
      with import nixpkgs { system = "x86_64-linux"; };
      python3.pkgs.buildPythonPackage rec {
        pname = "i3blocks_gcalcli";
        version = "0.1.0";
        src = self;
        doCheck = false;
        meta = {
          homePage = "https://github.com/PrimaMateria/i3blocks-gcalcli";
          description = "Shows upcoming event in the status bar and full month when clicked on.";
        };
        propagatedBuildInputs = [ python3.pkgs.dateutil python3.pkgs.click ];
      };
  };
}
