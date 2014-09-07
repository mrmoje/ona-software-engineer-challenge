/**
* Node.js/Javascript port of software engineering challenge answer.
*
* Requires underscore.js (npm install underscore)
*
* To run in node console:-
* var js_port = require('./javascript');
* js_port.calculate()
*  ~ or ~
* js_port.calculate(DATASET_URL)
*/

module.exports = {
    "calculate" : function calculate(url) {
        /**
        * Processes the data set and returns the required "summary" JSON object
        *
        * @param {String} url:A link to the JSON water points dataset 
        */
        console.log("Wait for it.......");
        url = typeof url !== 'undefined' ? url 
        :"https://raw.githubusercontent.com/onaio/ona-tech/master/data/water_points.json";

        var https = require('https');
        https.get(url, function (response) {
            var body = '';
            response.on('data', function (chunk) {body += chunk;});
            response.on('end', 
                function () {
                    var _ = require('underscore'), data_set = JSON.parse(body);
                    console.log( 
                        {
                            "number_functional": 
                                data_set.filter(
                                    function (x) {
                                        return x.water_functioning==="yes";
                                    }).length,
                            "number_water_points": 
                                _.countBy(data_set,
                                    function (x) {
                                        return x.communities_villages;
                                    }
                                ), 
                            "community_ranking": 
                                _.object(
                                    _.map(
                                        _.groupBy(data_set, 
                                            function (x) {
                                                return x.communities_villages;
                                            }
                                        ),
                                        function (v,k) {
                                            return [k, Math.ceil(100*v.filter(
                                                function (x) {
                                                    return x.water_functioning!=="yes";
                                                }).length/v.length)];
                                        }
                                    )
                                )
                        }
                    );
                }
            );
        }).on('error', function (e) { 
            data_set = []; console.log("Error: ", e);
        });
    }
};
