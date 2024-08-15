# Define the root of the local git clone for the common rules to be able 
# know where they are running from.
REPOROOT=../../..
# Include a library of common .transform.* targets which most
# transforms should be able to reuse.  However, feel free
# to override/redefine the rules below. 

# $(REPOROOT)/.make.versions file contains the versions

#TRANSFORM_NAME=doc_quality

include $(REPOROOT)/transforms/.make.transforms

TRANSFORMS_NAMES = code/code_quality \
    	code/code2parquet \
    	code/header_cleanser \
		code/code_quality \
		code/proglang_select \
		language/doc_chunk \
		language/doc_quality \
		language/lang_id \
		language/pdf2parquet \
		language/text_encoder \
		universal/ededup \
		universal/filter \
		universal/resize \
		universal/tokenization

venv: 
	$(MAKE) .defaults.create-venv
	source venv/bin/activate;       \
	$(PYTHON) -m pip install . 


test::	setup venv test-src

clean:: .transforms.clean
	-rm -fr src

image:: .transforms.python-image

test-src:: 
	source venv/bin/activate;       \
	for T in $(TRANSFORMS_NAMES); do                    \
	    echo running unit test on: $$T ; \
		$(PYTEST) $(REPOROOT)/transforms/$$T/python/test; \
	done;

test-with-pypi:
	$(MAKE) .defaults.create-venv
	source venv/bin/activate;       \
	$(PYTHON) -m pip install data_prep_toolkit_transforms==0.2.1.dev0 
	$(MAKE) test-src


setup: .transforms.setup 
	$(MAKE) src

src:
	for T in $(TRANSFORMS_NAMES); do                    \
	    echo copy src from  $$T ; \
		cp -R $(REPOROOT)/transforms/$$T/python/src/ src/ ; \
		rm -fr *.egg-info ; \
		rm -fr dist ; \
		rm -fr build ; \
	done;


build:: build-dist
        
publish:: publish-dist
        
build-dist:: setup .defaults.build-dist 

publish-dist:: .defaults.publish-dist


