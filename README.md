# Ducky
<h1 style="text-align: center;">Qwacker per Giuseppe</h1>
<p><br /><br />Usual procedure of importing requirements with</p>
<pre><em>pip install -r requirements.txt</em></pre>
<p>Then get the bot going BY PUTTING YOUR TOKEN and using</p>
<pre><em>python3 Qwack.py</em></pre>
<p>&nbsp;</p>
<p>TO DO:</p>
<ol>
<li>You will notice that it generate a shitload of "dirty", logs a lot of errors and warnings, they have to get fixed and I don't have time to keep up with them</li>
<li>It must be synchronized, the sessions do not close themselves
<pre>async def qwack</pre>
</li>
<li>The delete function of the sent images is weak, it use .pop randomly, it would be better to do it chronological starting from the oldest, it's a stupid thing to do but I'll let you think about it</li>
<li>Maybe the regex part is optimizable, maybe to list of occurrences and not to multiple instances, wrap it as you like</li>
<li>If you want to add features it would be more than appreciated</li>
</ol>
