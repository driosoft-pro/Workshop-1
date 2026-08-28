###############################################################
# flake.nix — Python Data Science Environment
# Python 3.12 + uv + Jupyter + NumPy + Pandas + PostgreSQL
###############################################################
{
  description = "Workshop 1 — Dimensional Data Warehouse for Recruitment Analytics";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      pythonEnv = pkgs.python312.withPackages (ps: with ps; [
        ipykernel
        pyzmq
        jupyter-client
        notebook
        ipywidgets
        numpy
        pandas
        matplotlib
        seaborn
        scikit-learn
        sqlalchemy
        psycopg2
        psycopg2-binary
        python-dotenv
        requests
        httpx
        pytest
        black
        flake8
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pythonEnv
          pkgs.uv
          pkgs.postgresql_16
          pkgs.stdenv.cc.cc.lib
          pkgs.zlib
        ];

        shellHook = ''
          if [ ! -d .venv ]; then
            uv venv --system-site-packages
          fi
          source .venv/bin/activate

          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.zlib ]}:$LD_LIBRARY_PATH"

          python -m ipykernel install --user --name=.venv --display-name "Python (uv .venv)" > /dev/null 2>&1

          echo ""
          echo "╔══════════════════════════════════════════════════════════╗"
          echo "║  Workshop 1 — Data Warehouse Recruitment Analytics      ║"
          echo "╚══════════════════════════════════════════════════════════╝"
          echo ""
          echo "Python:  $(python --version)"
          echo "uv:      $(uv --version)"
          echo "psql:    $(psql --version | head -1)"
          echo ""
          echo "Comandos:"
          echo "  jupyter lab              JupyterLab"
          echo "  jupyter notebook         Notebook clasico"
          echo "  python src/main.py       Ejecutar pipeline ETL"
          echo "  uv pip install <pkg>     Instalar paquete"
          echo ""
          echo "Stack: NumPy, Pandas, Matplotlib, Scikit-learn, SQLAlchemy, psycopg2"
          echo ""
        '';
      };
    };
}
