Summer
======

Ever wanted to do in a quick list of numbers, maybe having a bit of annotation
here and there? Big spreadsheets are way too big to be comfy and they won't
even support vi keys! And the great little sc might be too little for our
purposes.

Enter Summer, a Vim plugin with a bit of arithmetic functionality that allows
you to write your notes in natural languages and Summer picks up the numerical
bits. I actually wanted to just use the nice-looking Soulver but it's for Mac
only. Hence, Summer.

So, what can you do?
--------------------

- Just throw in numbers like this: 200
- Make calculations inside angle brackets: ``<200/2 = 100>``
- Define variables the following manner::

        @var 100
        @foo <200+30 = 230>

- Use those variables in further calculations::

        <@var + @foo = 330>

- Use the predefined variables well::

        <@sum = 960>

- Comment lines with ``;`` so that the variables don't define.
- Mark lines with ``--`` (as the first or the last thing) to keep numbers from
  accumulating in ``@sum``.
- Use words after numbers to mark their types. Use ``<@sum:type>`` to
  accumulate per type. For instance::

        4 balls
        6 towels
        <@sum:balls = 4>

- Use automatically set variables ``_`` or ``@ans`` to recall last evaluated
  result like this::

        <100+40 = 140> eur
        <_ - 22 = 118>

INSTALLATION
------------

Copy the stuff from ``vim-summer/`` to your ``~/.vim/``. Pathogen is
recommended! Set the path to your copy of 'summer.py' in ``.vimrc`` in the
variable ``g:summer_parser``.  Now you can set any buffer's filetype to
"summer".  Alternatively edit a ".sum" ended file and Vim will apply the
filetype to it.

USAGE
-----

Three key bindings are provided:

=====================   =====================================================
``<Localleader>e``      re-evaluate the buffer.
``<Localleader>c``      toggle the current line commented or not.
``<Localleader>a``      toggle the accumulate mark on the current line.
=====================   =====================================================

The existing Vim normal mode maps ``<C-a>`` and ``<C-x>`` have been remapped to
instantly refresh the buffer after incrementing or decrementing a number.

I'm not sure what the default for ``<Localleader>`` is, so you can make
sure it's something sensible by setting up ``maplocalleader = ','`` in your
``.vimrc``::

    let maplocalleader = ','

TIPS
----

For bash and zsh::

    alias Summer='vim -c ":set filetype=summer"'

BUGS AND ISSUES
---------------

See TODO (and the source :)

