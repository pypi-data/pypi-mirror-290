# codi-cooperatiu-internal-tools
Eines i mòduls interns de Codi Cooperatiu

## flowbite_css

`flowbite_css` aplica personalitzacions de formulari automàticament. Aquesta personalització fa servir estils de Flowbite, una personalització de Tailwind.

### Configuració

Per fer servir aquestes personalitzacions, hem d'afegir l'aplicació `flowbite_css` al paràmetre `INSTALLED_APPS` del fitxer `settings.py`.

#### CODI_COOP_ENABLE_MONKEY_PATCH

El paràmetre `CODI_COOP_ENABLE_MONKEY_PATCH` en el fitxer `settings.py` controla si s'ha d'aplicar o no un monkey patch als camps de formulari de Django dins la vostra aplicació.

Per defecte, el paràmetre `CODI_COOP_ENABLE_MONKEY_PATCH` està desactivat (`False`). Això significa que el monkey patch no s'aplicarà. Si voleu activar el monkey patch, heu d'afegir el paràmetre `CODI_COOP_ENABLE_MONKEY_PATCH` al fitxer `settings.py` i establir-lo a `True`.

#### Exemples:

**Activar el monkey patching:**

```python
# settings.py

CODI_COOP_ENABLE_MONKEY_PATCH = True
```

Quan aquest paràmetre està activat (`True`), els camps de formulari de Django com `CharField`, `EmailField`, `IntegerField`, `ChoiceField`, `MultipleChoiceField`, i `BooleanField` utilitzaran els camps personalitzats definits en la vostra aplicació (`CharBoundField`, `BooleanBoundField`, etc.), permetent un estil i comportament personalitzats en els vostres formularis.

**Desactivar el monkey patching:**

```python
# settings.py

CODI_COOP_ENABLE_MONKEY_PATCH = False  # Valor per defecte
```

Si aquest paràmetre està desactivat (False), els camps de formulari de Django funcionaran amb el seu comportament i estil per defecte, sense cap personalització addicional.

#### FORM_RENDERER

També tenim la possibilitat de fer servir la plantilla personalitzada que mostra tot el HTML vinculat amb els camps (`<label />` i qualsevol altre HTML) amb classes de Flowbite.
En aquest cas, hauríem de fer servir el *form render* `CustomFormRenderer` configurant-ho al fitxer `settings.py` amb el parametre `FORM_RENDERER`:

```python
# settings.py

FORM_RENDERER = "flowbite_css.renderers.CustomFormRenderer"
```

# Contribució
## Instal·la els requisits

Instal·la les dependències per al desenvolupament anant a la carpeta «codi-cooperatiu-internal-tools» i després s'executa:

```commandline
pip install -r requirements.txt
```

A més d'aquests requisits també hauràs d'instal·lar el propi Django. Per a instal·lar la versió actual de Django:

```commandline
pip install django
```

El codi ve amb git hook scripts. Aquests es poden instal·lar executant-se:

```commandline
pre-commit install
```

El pre-commit ara s'executarà automàticament al fer git-commit i comprovarà l'adhesió a la guia d'estil (black, isort i flake8).

## Executa les proves

Abans d'enviar una pull request, executeu tot el conjunt de proves «codi-cooperatiu-internal-tools» via:

```commandline
make test
```

Si no teniu instal·lat el `make`, el conjunt de proves també es pot executar via:

```commandline
pytest --ds=tests.test_settings --cov=flowbite_classes
```