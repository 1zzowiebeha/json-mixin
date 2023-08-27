# json-mixin
A mixin that will allow you to serialize &amp; deserialize arbitrary python objects

To use, simply import `jmixin` and inherit from `JSerializer`!

Warning: Be cautious when parsing JSON data from untrusted sources. A malicious JSON string may cause the decoder to consume considerable CPU and memory resources. Limiting the size of data to be parsed is recommended. (source: https://docs.python.org/3/library/json.html)
