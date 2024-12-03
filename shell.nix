with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python3.withPackages (ps: with ps; [
            black
            flake8
            matplotlib
            pandas
            scikitlearn
            seaborn
        ]))
        (with rPackages; [
            coda
            codetools
            mvtnorm
            R
            rstan
        ])
        csvkit
        feh
        glibcLocales
        jq
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
    hardeningDisable = [ "all" ];
}
