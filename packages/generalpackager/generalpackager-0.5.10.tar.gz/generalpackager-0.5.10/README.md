<details open>
<summary><h1>generalpackager</h1></summary>

Tools to interface GitHub, PyPI, NPM and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for ManderaGeneral for now.

<details>
<summary><h2>Table of Contents</h2></summary>

<pre>
<a href='#generalpackager'>generalpackager</a>
├─ <a href='#Dependency-Diagram-for-ManderaGeneral'>Dependency Diagram for ManderaGeneral</a>
├─ <a href='#Installation-showing-dependencies'>Installation showing dependencies</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Attributes'>Attributes</a>
├─ <a href='#Contributions'>Contributions</a>
└─ <a href='#Todo'>Todo</a>
</pre>
</details>


<details open>
<summary><h2>Dependency Diagram for ManderaGeneral</h2></summary>

```mermaid
flowchart LR
0([import]) --> 3([file])
0([import]) --> 2([library])
1([tool]) --> 2([library])
3([file]) --> 4([packager])
2([library]) --> 4([packager])
2([library]) --> 3([file])
click 0 "https://github.com/ManderaGeneral/generalimport"
click 1 "https://github.com/ManderaGeneral/generaltool"
click 2 "https://github.com/ManderaGeneral/generallibrary"
click 3 "https://github.com/ManderaGeneral/generalfile"
click 4 "https://github.com/ManderaGeneral/generalpackager"
style 4 stroke:#482
```
</details>


<details open>
<summary><h2>Installation showing dependencies</h2></summary>

| `pip install`                                                                      | `generalpackager`   |
|:-----------------------------------------------------------------------------------|:--------------------|
| <a href='https://pypi.org/project/generallibrary[table]'>generallibrary[table]</a> | ✔️                  |
| <a href='https://pypi.org/project/generalfile'>generalfile</a>                     | ✔️                  |
| <a href='https://pypi.org/project/requests'>requests</a>                           | ✔️                  |
| <a href='https://pypi.org/project/pyinstaller'>pyinstaller</a>                     | ✔️                  |
| <a href='https://pypi.org/project/coverage'>coverage</a>                           | ✔️                  |
| <a href='https://pypi.org/project/setuptools'>setuptools</a>                       | ✔️                  |
| <a href='https://pypi.org/project/wheel'>wheel</a>                                 | ✔️                  |
| <a href='https://pypi.org/project/twine'>twine</a>                                 | ✔️                  |
</details>


<details open>
<summary><h2>Information</h2></summary>

| Package                                                              | Ver                                                 | Latest Release       | Python                                                                                                                                                                                                                                                                                                                | Platform        | Cover   |
|:---------------------------------------------------------------------|:----------------------------------------------------|:---------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|:--------|
| [generalpackager](https://github.com/ManderaGeneral/generalpackager) | [0.5.10](https://pypi.org/project/generalpackager/) | 2024-01-24 07:20 CET | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/), [3.11](https://www.python.org/downloads/release/python-3110/), [3.12](https://www.python.org/downloads/release/python-3120/) | Windows, Ubuntu | 69.1 %  |
</details>



<details>
<summary><h2>Attributes</h2></summary>

<pre>
<a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/__init__.py#L1'>Module: generalpackager</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L54'>Method: api_url</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L23'>Method: format_version</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L138'>Method: get_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L125'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L113'>Method: get_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L58'>Method: git_clone_command</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L40'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L36'>Method: name_is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L76'>Property: pip_install_command</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L150'>Method: request_kwargs</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L144'>Method: set_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L131'>Method: set_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L119'>Method: set_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L45'>Property: simple_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L51'>Property: ssh_url</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L18'>Method: tag_is_version</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L27'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L68'>Method: get_all_local_modules</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L90'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L75'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L21'>Property: module</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L42'>Property: objInfo</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/#L426'>Property: path</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L8'>Class: Targets</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: changed_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: clone</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: commit</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/commit_editmsg.py#L5'>Class: commit_editmsg_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L11'>Method: commit_message</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: commit_sha</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L76'>Method: commit_sha_short</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/examples.py#L5'>Class: examples_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/exeproduct.py#L5'>Class: exeproduct_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/exetarget.py#L5'>Class: exetarget_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L45'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L104'>Method: format_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/generate.py#L6'>Class: generate_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L88'>Method: get_all_versions</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L88'>Method: get_examples_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L56'>Method: get_exeproduct_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L52'>Method: get_exetarget_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L27'>Method: get_file_from_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L11'>Method: get_filenames</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L17'>Method: get_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L22'>Method: get_files_by_relative_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L48'>Method: get_generate_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L16'>Method: get_git_exclude_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L60'>Method: get_git_ignore_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L68'>Method: get_index_js_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L44'>Method: get_init_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L28'>Method: get_license_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L24'>Method: get_manifest_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L12'>Method: get_metadata_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L64'>Method: get_npm_ignore_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L8'>Method: get_org_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L76'>Method: get_package_json_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L62'>Method: get_package_paths_gen</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L80'>Method: get_pre_commit_hook_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L84'>Method: get_pre_push_hook_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L4'>Method: get_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L20'>Method: get_setup_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L72'>Method: get_test_js_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L36'>Method: get_test_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L56'>Method: get_test_paths</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L40'>Method: get_test_template_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_paths.py#L32'>Method: get_workflow_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L28'>Method: git_config</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/git_exclude.py#L5'>Class: git_exclude_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L20'>Method: git_missing_credentials</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_git.py#L24'>Method: git_nothing_to_commit</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/gitignore.py#L5'>Class: gitignore_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/index_js.py#L6'>Class: index_js_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: init</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/init.py#L6'>Class: init_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L28'>Method: is_django</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L32'>Method: is_exe</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L40'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L24'>Method: is_node</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L20'>Method: is_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/license.py#L6'>Class: license_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/manifest.py#L5'>Class: manifest_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L34'>Property: metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L38'>Method: metadata_exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/metadata.py#L5'>Class: metadata_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L36'>Method: name_is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/npm_ignore.py#L5'>Class: npm_ignore_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/org_readme.py#L6'>Class: org_readme_file</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/org_readme.py#L18'>Method: get_org_description_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/package_json.py#L6'>Class: package_json_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/pre_commit_hook.py#L4'>Class: pre_commit_hook_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/pre_push_hook.py#L6'>Class: pre_push_hook_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/decos.py#L4'>Method: push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L8'>Class: readme_file</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L125'>Method: get_attributes_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L17'>Method: get_badges_dict</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L246'>Method: get_contributions_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L27'>Method: get_description_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L89'>Method: get_examples_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L195'>Method: get_footnote_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L219'>Method: get_information_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L44'>Method: get_installation_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L209'>Method: get_mermaid_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L163'>Method: get_todos</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L169'>Method: get_todos_markdown</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L204'>Method: github_link</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L137'>Method: github_link_path_line</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L189'>Method: set_collapsible</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L50'>Method: repo_exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/setup.py#L6'>Class: setup_file</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/setup.py#L21'>Method: get_classifiers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L45'>Property: simple_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo_target.py#L18'>Method: targetted</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test.py#L5'>Class: test_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test_js.py#L6'>Class: test_js_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test_template.py#L6'>Class: test_template_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/workflow_dev.py#L4'>Class: workflow_dev_file</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/workflow.py#L8'>Class: workflow_file</a>
│     └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/workflow.py#L16'>Method: codeline</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/node/localrepo_node.py#L9'>Class: LocalRepo_Node</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L12'>Class: LocalRepo_Python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L17'>Method: get_python_exe_path</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L57'>Method: set_easy_install_value</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L37'>Class: Packages</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L62'>Method: all_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L8'>Class: Targets</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L22'>Method: commit_and_push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/commit_editmsg.py#L5'>Class: commit_editmsg_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L38'>Method: compare_local_to_github</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L45'>Method: compare_local_to_pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L7'>Method: create_blank_locally</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L34'>Method: create_github_repo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L38'>Method: create_master_branch</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/examples.py#L5'>Class: examples_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/exeproduct.py#L5'>Class: exeproduct_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/exetarget.py#L5'>Class: exetarget_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L77'>Method: general_bumped_set</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L85'>Method: general_changed_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/generate.py#L6'>Class: generate_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L61'>Method: generate_localfiles</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_metadata.py#L29'>Method: get_classifiers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L38'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L23'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L27'>Method: get_file_from_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L11'>Method: get_filenames</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L17'>Method: get_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/shared_files.py#L22'>Method: get_files_by_relative_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_pypi.py#L8'>Method: get_latest_release</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L49'>Method: get_ordered_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L71'>Method: get_owners_package_names</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_metadata.py#L6'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/git_exclude.py#L5'>Class: git_exclude_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L81'>Property: github</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L49'>Method: github_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/gitignore.py#L5'>Class: gitignore_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L71'>Method: if_publish_bump</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L78'>Method: if_publish_upload</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/index_js.py#L6'>Class: index_js_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/init.py#L6'>Class: init_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_metadata.py#L35'>Method: is_bumped</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L28'>Method: is_django</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L32'>Method: is_exe</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L40'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L24'>Method: is_node</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L20'>Method: is_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/license.py#L6'>Class: license_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L88'>Property: localmodule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L54'>Method: localmodule_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L73'>Property: localrepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L44'>Method: localrepo_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/manifest.py#L5'>Class: manifest_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/metadata.py#L5'>Class: metadata_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L36'>Method: name_is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_environment.py#L9'>Method: new_clean_environment</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/npm_ignore.py#L5'>Class: npm_ignore_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/org_readme.py#L6'>Class: org_readme_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/package_json.py#L6'>Class: package_json_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_relations.py#L11'>Method: packagers_from_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/pre_commit_hook.py#L4'>Class: pre_commit_hook_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/pre_push_hook.py#L6'>Class: pre_push_hook_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L14'>Method: push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L95'>Property: pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L62'>Method: pypi_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L8'>Class: readme_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_pypi.py#L23'>Method: reserve_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L22'>Method: run_ordered_methods</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/setup.py#L6'>Class: setup_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L45'>Property: simple_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L36'>Method: summary_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L6'>Method: sync_github_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_metadata.py#L50'>Property: target</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test.py#L5'>Class: test_folder</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test_js.py#L6'>Class: test_js_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/test_template.py#L6'>Class: test_template_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L66'>Method: upload_package_summary</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/workflow_dev.py#L4'>Class: workflow_dev_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/workflow.py#L8'>Class: workflow_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L18'>Method: workflow_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L7'>Method: workflow_sync</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L7'>Method: workflow_unittest</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L13'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localmodule.py#L9'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L17'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L27'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L40'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L36'>Property: json_endpoint</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L36'>Method: name_is_general</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/name.py#L45'>Property: simple_name</a>
└─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L9'>Class: Venv</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L69'>Method: active</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L72'>Method: create_venv</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv_cruds.py#L69'>Property: cruds</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L85'>Method: deactivate</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L171'>Method: debug</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L54'>Method: easy_install_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L48'>Method: exe_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L66'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L30'>Method: get_active_python</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L18'>Method: get_active_venv</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L24'>Method: get_active_venv_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L131'>Method: list_python_versions</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L120'>Method: list_venv_paths</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L52'>Method: python_exe_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L56'>Method: python_home_exe_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L55'>Method: python_home_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L60'>Method: python_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L58'>Method: python_sys_executable_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L117'>Method: python_version</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L50'>Method: pyvenv_cfg_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L51'>Method: scripts_path</a>
   └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/venv.py#L53'>Method: site_packages_path</a>
</pre>
</details>


<details open>
<summary><h2>Contributions</h2></summary>

Issue-creation, discussions and pull requests are most welcome!
</details>


<details>
<summary><h2>Todo</h2></summary>

| Module                                                                                                                                                      | Message                                                                                                                                                                                                          |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L1'>packager_files.py</a>                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L9'>Fix create_blank, it overwrites current projects pip install.</a>                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L1'>packager_api.py</a>                              | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_api.py#L43'>Check that every API has create an *_available method</a>                                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L1'>packager_github.py</a>                        | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L44'>Setup env vars for project.</a>                                                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L1'>localrepo_python.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L77'>Make sure twine is installed when trying to upload to pypi.</a>             |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L1'>localrepo_python.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L78'>Look into private PyPI server where we could also do dry runs for test.</a> |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L1'>localrepo.py</a>                 | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L22'>Search for imports to list dependencies.</a>                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L1'>readme.py</a>             | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/files/definitions/readme.py#L166'>Sort todos by name to decrease automatic commit changes.</a>                 |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L1'>target.py</a>                               | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/shared/target.py#L39'>Generate Python file in generalpackager containing general packages.</a>                        |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L1'>pypi.py</a>                            | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L13'>Move download to it's own package.</a>                                                     |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L1'>pypi.py</a>                            | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/pypi.py#L78'>Find a faster fetch for latest PyPI version and datetime.</a>                              |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L1'>github.py</a>                        | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/package_hosts/github.py#L15'>Get and Set GitHub repo private.</a>                                                     |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                                      | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L25'>Define license in one place</a>                                                                          |
</details>


<sup>
Generated 2024-01-24 07:20 CET for commit <a href='https://github.com/ManderaGeneral/generalpackager/commit/master'>master</a>.
</sup>
</details>

