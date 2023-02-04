import { JSDOM, ResourceLoader } from "jsdom";
import CryptoJS from 'crypto-js';
import fs from "fs";
import express from 'express';

const app = express()
const port = 1337

// const signature_js = fs.readFileSync(
//     "./sdk/signature.js",
//     "utf-8"
// );

const webmssdk = fs.readFileSync(
    "./sdk/webmssdk.js",
    "utf-8"
);


app.get('/', (req, res) => {
    var start = performance.now();

    const url = req.query.url;
    const userAgent = req.query.user_agent;

    console.log(req.query.url);
    console.log(req.query.user_agent);

    if (typeof url !== "undefined" && typeof userAgent !== "undefined") {

        if (url === "") {
            return res.send({
                "success": false,
                "error": "url can't be empty."
            })
        }

        if (userAgent === "") {
            return res.send({
                "success": false,
                "error": "user_agent can't be empty."
            })
        }

        try {
            const resourceLoader = new ResourceLoader({
                userAgent: userAgent
            });

            const { window } = new JSDOM(``, {
                url: "https://www.tiktok.com/",
                referrer: "https://www.tiktok.com/",
                contentType: "text/html",
                includeNodeLocations: false,
                runScripts: "outside-only",
                pretendToBeVisual: true,
                resources: resourceLoader,
            });

            // _window.eval(signature_js.toString());
            // _window.byted_acrawler.init({
            //     aid: 24,
            //     dfp: true,
            // });
            window.eval(webmssdk);

            // var sig = _window.byted_acrawler.sign({ url });
            var xbogus = window._0x32d649(url.split("?")[1]);
            // var tt_params = encryptationData(url.split("?")[1]);

            var duration = performance.now() - start;
            console.log("duration", duration);

            return res.send({
                "success": true,
                // "X-Bogus": xbogus,
                // "_signature": sig,
                // "x-tt-params": tt_params,
                "signed_url": url + "&X-Bogus=" + xbogus //+ "&_signature=" + sig
            })
        } catch (err) {
            console.log("ERR!", err);
            return res.send({
                "success": false,
                "error": "an error occured"
            })
        }
    } else {
        return res.send({
            "success": false,
            "error": "url and user_agent are required."
        })
    }
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})