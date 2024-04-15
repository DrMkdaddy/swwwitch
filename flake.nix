{
  description = "Nix-flake to change my wallpapers. :3 Send a PR to make this more malleable or something.";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication;
    in {
      packages = {
        swwwitch = mkPoetryApplication {projectDir = self;};
        default = self.packages.${system}.swwwitch;
      };

      devShells.default = pkgs.mkShell {
        inputsFrom = [self.packages.${system}.swwwitch];
        packages = [pkgs.poetry];
      };
    });
}
