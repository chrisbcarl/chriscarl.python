# TODO

- ARGHHHH
    - everything is fucking broken in `dev audit cov` somehow, its creating files and shit


- FEATURES
    unittest
        on failed unit test, print the experiment on the left, the control on the right, vars if you have to...

    subprocess
        monitor the file, see if its size hasn't increased in seconds, then auot-kill

    are new features added that arent in the FEATURES doc?
    are all prod features in the commit messages?
    move all staged features to prod
        change dates
        change version
- dev

    dict indexing should allow for regex... dict['.*']

    make a scan for stackoverflow thing and from there, generate a list of credits in the readme or elsewhere

    the last thing I was on is trying to compare one file to another via AST, see if functions were added / removed, so I can autogen the changelog
    dict probably should redo flatten in the context of walk to get all of the keys...

    dev new project
        creates a pre-commit
        creates the .vscode
        creates the extensions, etc.
        pyproj toml
        mypy --install-types --non-interactive

    def new namespace core.lib.third.pandas
        where the implication is a new namespace project is made that creates a core.pandas and a mod.pandas just in case
            ```python
            def text_to_df(text):
                lines = text.splitlines()
                columns = [ele.strip() for ele in lines[0].split('\t') if ele.strip()]
                data = lines[1:]
                mat = [line.split('\t')[1:] for line in data]
                for r, row in enumerate(mat):
                    for c, col in enumerate(row):
                        mat[r][c] = col.strip()
                        try:
                            mat[r][c] = int(col.strip())
                        except ValueError:
                            pass
                df = pd.DataFrame(mat, columns=columns)
                return df

            text = '''  customer        category        important       sales
            0   101     cat2    yes     123
            1   102     cat2    no      52
            2   103     cat1    yes     214
            3   104     cat3    yes     663
            4   101     cat2    yes     204
            5   103     cat1    yes     453'''
            ```
    an uber class: UberObject
        has to_dict, to_str, to_yaml, to_ini, from_ini, to_argparse, from_argparse, etc. to pickle, from pickle, etc.
        also has privates that can be omitted from string representations, and privates that say particular values are to be printed in an encrypted way
        have data model things like +, *, -, diff, etc.

    version class is fucked, please simplify
    some kind of exception class that is able to raise exceptions cleanly, with correct relevant traceback localization
        exc_info = sys.exc_info()
        traceback = exc_info[2]
        back_frame = traceback.tb_frame.f_back
        back_tb = TracebackType(tb_next=None, tb_frame=back_frame, tb_lasti=back_frame.f_lasti, tb_lineno=back_frame.f_lineno)
        .with_traceback(back_tb)
        .with_traceback(back_tb)
        .with_traceback(exe.__traceback__)
    audit imports
        test all imports this way:
            modules = walk_module_names_filepaths
            for modules in modules:
                subprocess.popen(python -c import module)
    do pyi stubgen myself with AST analysis and figure out what i've added or changed and then modify the ast directly and THEN print it out.
        basically analyze the AST of original module
        analyze AST of shadow module
        combine what has been changed or added in the new ast
        import ast
        with open(r'C:\Users\chris\src\chriscarl-python\dist\typing\logging\__init__.pyi') as r:
            content = r.read()
        parsed = ast.parse(content)
        print(ast.dump(parsed, indent=4))
        print(ast.unparse(parsed))
    mod.all created
        on new mod.something, add it to all
        edit the templates so that they use all
    mod.logging needs to modify all previously instantiated loggers with the new logger class so they get all level functions...
    full / all
    new hermione
        scan for changes, make sure theres a documentation that correlates with that.
    commit, does all of the pre-commit and other shit i need to do
    implement the full workflow, partial workflow, etc.
    tdd add something to verify the main section includes all functions either commented or not
        ```python
        import tests
        from tests.chriscarl.mod.lib.stdlib.test_logging import TestCase
        tc = TestCase()
        [ele for ele in dir(tc) if ele.startswith('test')]
        ['test_case_0_ungabunga']
    create should probably be template and name based, with changable rules, and the template explains how to parse and how to imply what that path arg is (that way other projects can use it by specifying a template dirpath)
        dev create lib chriscarl.core.types.bigint
        dev create mod chriscarl.mod.lib.logging
        dev create ipynb scripts/notes/etc --template-dir ./project/create/templates --rule-dir ./project/create/rules
            where there's an implied ipynb within templates and rules

func to cli
  would be nice if I could just make a cli out of a function's parameters and help...

  dev run only runs parameterless functions
  dev run core.functors.parse.latex.evaluate -h

cli latex calculator

- on commit
    scan for and replace / remove
        f' strings - f'\w
    stubgen src\chriscarl -o dist/typing
    make sure all files in files have a corresponding constant
- logging
    ```python
    console_log(lognames=[__name__, 'chriscarl'], level=logging.VERBOSE)  # pylint: disable=no-member
    change to console_log()  # which defaults to __name__, level verbose
    LOGGER.info('this is a cannonical way of making files here.')
    ```
    - self modifying format that elongates its prints based on the last longest and internally justifies
- git workflow (cicd pipelining): https://github.com/chrisbcarl/chriscarl-python/new/main?filename=.github%2Fworkflows%2Fpython-app.yml&workflow_template=ci%2Fpython-app
- multiversion python package "workflow":https://github.com/chrisbcarl/chriscarl-python/new/main?filename=.github%2Fworkflows%2Fpython-package.yml&workflow_template=ci%2Fpython-package


- typing stub creation
    ```
    # https://stackoverflow.com/questions/76898602/mypy-stub-files-and-vs-code
    # https://stackoverflow.com/questions/41915404/packaging-stub-files
    ```
- look into requirement usages that i've used before and knock them out:
    - app dev: jinja2, xmljson, markdown, sqlalchemy, pyodbc, pywinauto, pywin32, libpqxx-dev, g++, unixodbc-dev, wxPython
    - python metatyping: mypy, pyinstaller, GitPython, pytest-cov,
    - python building: check-manifest
    - python 2 backports: future, pathlib, typing, configparser, enum-compat,funcsigs, regex
- order by category, name, etc.
    - say you have a complex list of text entries, and each entry belongs to a category, and you want to sort them by harm at the top
    - ['lithium', 'iron', 'boron', 'nitrogen', 'uranium', 'titanium']
    - ['lithium', 'uranium', 'iron', 'nitrogen', 'titanium', 'boron']
- analyze an ipynb and add anchors and all kinds of nice navigation shit - like each markdown always has a link at the bottom to go back up to the top, or to go to the next section and what that next section is etc.
    ```python
    with open(r'shit.ipynb') as r:
        ipynb = json.load(r)
    for cell in ipynb['cells']:
        if cell['cell_type'] == 'markdown':
            last_line = cell['source'][-1]
            if 'go to top' not in last_line.lower():
                cell['source'].append('')
                cell['source'].append('[Go to Top](#top)')
            elif 'go to top' in last_line.lower():
                cell['source'][-1] = '<a href="#top">Go to Top</a>'

    with open(r'shit.ipynb', 'w') as w:
        json.dump(ipynb, w, indent=2)
    ```