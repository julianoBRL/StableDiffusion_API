FROM python
WORKDIR /Stable_Diffusion
EXPOSE 9000
ADD ./* /Stable_Diffusion/
ADD ./src/* /Stable_Diffusion/src/

ADD ./src/controllers/* /Stable_Diffusion/src/controllers/
ADD ./src/models/* /Stable_Diffusion/src/models/
ADD ./src/services/* /Stable_Diffusion/src/services/

RUN pip install transformers flask torch diffusers python-slugify
ENTRYPOINT python main.py flask run