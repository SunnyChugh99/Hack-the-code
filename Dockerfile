FROM 359328299697.dkr.ecr.us-east-1.amazonaws.com/mosaic-ai-logistics/mosaic-notebooks-manager/git:1.0.14.1_git_hub
RUN rm -rf /usr/src/ml-autotagging/models/*
COPY models/* /usr/src/ml-autotagging/models/
