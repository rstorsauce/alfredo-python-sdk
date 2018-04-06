To get the latest version of the `alfredo-python-sdk`, branch `laurel_demo`:

     ~/dev/git/rstor/ $ git clone https://github.com/rstorsauce/alfredo-python-sdk.git
     ~/dev/git/rstor/alfredo-python-sdk (develop u=) $ git checkout laurel_demo
     ~/dev/git/rstor/alfredo-python-sdk (laurel_demo u=) $


To install a local version of a library, instead of a published one, execute `pip install -e <path>` from the `alfredo-api` root:

     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ pip install -e /home/rober/dev/git/rstor/alfredo-python-sdk/
    Obtaining file:///home/rober/dev/git/rstor/alfredo-python-sdk
    Requirement already satisfied: requests in ./.virtualenv/lib/python2.7/site-packages (from alfredo-python===0.0.3-laurel)
    Requirement already satisfied: ruamel.yaml in ./.virtualenv/lib/python2.7/site-packages (from alfredo-python===0.0.3-laurel)
    Requirement already satisfied: docopt in ./.virtualenv/lib/python2.7/site-packages (from alfredo-python===0.0.3-laurel)
    Requirement already satisfied: urllib3<1.23,>=1.21.1 in ./.virtualenv/lib/python2.7/site-packages (from requests->alfredo-python===0.0.3-laurel)
    Requirement already satisfied: idna<2.7,>=2.5 in ./.virtualenv/lib/python2.7/site-packages (from requests->alfredo-python===0.0.3-laurel)
    Requirement already satisfied: chardet<3.1.0,>=3.0.2 in ./.virtualenv/lib/python2.7/site-packages (from requests->alfredo-python===0.0.3-laurel)
    Requirement already satisfied: certifi>=2017.4.17 in ./.virtualenv/lib/python2.7/site-packages (from requests->alfredo-python===0.0.3-laurel)
    Requirement already satisfied: ruamel.ordereddict in ./.virtualenv/lib/python2.7/site-packages (from ruamel.yaml->alfredo-python===0.0.3-laurel)
    Requirement already satisfied: typing in ./.virtualenv/lib/python2.7/site-packages (from ruamel.yaml->alfredo-python===0.0.3-laurel)
    Installing collected packages: alfredo-python
      Found existing installation: alfredo-python 0.0.3
        Uninstalling alfredo-python-0.0.3:
          Successfully uninstalled alfredo-python-0.0.3
      Running setup.py develop for alfredo-python
    Successfully installed alfredo-python
    You are using pip version 9.0.1, however version 9.0.3 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.

Test if the installation was successful:

     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ cat .virtualenv/lib/python2.7/site-packages/alfredo-python.egg-link
    /home/rober/dev/git/rstor/alfredo-python-sdk

And check the version installed, both from the CLI and for the SDK:

     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ alfredo --version
    0.0.3-laurel
     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ python <<< 'import alfredo; print alfredo.__version__'
    0.0.3-laurel

If you want to use alfredo CLI and/or SDK against a local installation, please use the specific ENV vars.

     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ RUOTE_ROOT=http://localhost:8000 alfredo logout
     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ RUOTE_ROOT=http://localhost:8000 alfredo login
    Enter input:
    email: roy.batty@teamjamon.com
    password: *********
    ^D
     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ RUOTE_ROOT=http://localhost:8000 alfredo ruote apps id:6
    additional_information: []
    builduuid: null
    compressed_container_checksum: c66cab8c54b60430ab206f7b936219ee
    compression_software: gzip
    container_checksum: 2169d74e1444fcef96805b359e672a5e
    container_name: 20171130172234-yap.img.gz
    container_size: null
    container_url: http://minio.teamjamon.com/previrgo/20171130172234-yap.img.gz
    created: '2018-02-14T11:44:57Z'
    datasets: []
    description: ''
    enabled: true
    id: 6
    is_container_compressed: true
    is_container_validated: true
    log: http://localhost:8000/apps/6/log/
    name: aa-yap-vv
    owner: roy.batty@teamjamon.com
    public: true
    settings:
    - attribute: MPI name
      id: 1
      type: Requirement
      value: Open MPI
    - attribute: MPI version
      id: 2
      type: Requirement
      value: 1.6.5
    uuid: ab517e8e-807b-4bb8-8b3e-81dc04010808
    version: ''

To update a job:

     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ RUOTE_ROOT=http://localhost:8000 alfredo ruote -C update_job -i '{"uuid": "7f95a15d-a3ff-4e6b-b54b-4d8b327e19f4", state: "Completed"}'
    detail: Job state updated
     ~/dev/git/rstor/rstor/service/python/ruote (laurel_demo u=) $ RUOTE_ROOT=http://localhost:8000 python
    Python 2.7.12 (default, Nov 19 2016, 06:48:10)
    [GCC 5.4.0 20160609] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import alfredo
    >>> ruote = alfredo.ruote('3a4ee21e973421b334f0d55bb7c4e2051998eee6')
    >>> ruote.jobs[0].uuid
    u'7f95a15d-a3ff-4e6b-b54b-4d8b327e19f4'
    >>> ruote.update_job.create(uuid='7f95a15d-a3ff-4e6b-b54b-4d8b327e19f4', state='Failed')

    200 - OK

    detail: Job state updated
