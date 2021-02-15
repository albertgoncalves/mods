with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python38.withPackages(ps: with ps; [
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
}
