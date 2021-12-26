# Crossword Stats Website Backend

[![build status](https://img.shields.io/github/workflow/status/kesyog/crossword/Build?style=flat-square)](https://github.com/nicwineburger/crossword/actions/workflows/build.yml)
[![Apache 2.0 license](https://img.shields.io/github/license/kesyog/crossword?style=flat-square)](./LICENSE)

This is a fork of [keysog's crossword scraper](https://github.com/kesyog/crossword) and provides the backend for the [crosswordstats.com](crosswordstats.com) website. We've hooked up this repo to an AWS CodeBuild application that pulls when there is a merge into main, builds the image, and pushes the new image to an AWS Lambda function that serves as our endpoint for the frontend to hit. 

We made some changes to this backend to make it more performant for our needs. The frontend requests data in chunks and we fetch those chunks from the New York Times API at a slightly faster rate (though this might change in the future if the website has more traffice than expected).

If you have any requests or contributions please make a new branch and a PR. Feel free to contact me with any issues/ideas.

For more details on how this backend works please check out [kesyog's original README](https://github.com/kesyog/crossword/blob/main/README.md) as it has much more information.
