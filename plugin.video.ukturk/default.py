exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("ODEgMTksN2YsMTIsMTJjLDEzMiwxNiwxMDYsMzYsMmEsNDUsODQKZGQgZDEuMTIzLmI2IDgxIDk3CmRkIGI5IDgxIDY2CgozNyAgICAgICAgPSAnMTA5Ljc3LjEwOCcKMTQgICAgICAgPSA3Zi45NyhlNT0zNykKY2EgICAgICAgICAgID0gOTcoMzcsIDJhLjFhKQo2ICAgICAgICAgID0gMTkuNjAoMTA2LmU5LmRlKCc5ZjovL2U4L2FkLycgKyAzNyAsICc2LjEzOScpKQplMSAgICAgICAgICAgID0gMTkuNjAoMTA2LmU5LmRlKCc5ZjovL2U4L2FkLycgKyAzNywgJ2UxLmQyJykpCjlkICAgICAgICAgPSAnZGY6Ly9hYi42ZC4xMjIvYTcvNjQuZDQnCjY4ICAgICAgICA9IDE0LjI0KCdiZicpCjMwICAgICAgID0gMTQuMjQoJzQ5JykKNjMgICAgICAgPSBjYS5mNC4xMzYoJzYzJywgJycpCjk4ID0gNjYuZTYoYmQ9NGYpCmE0ID0gMTQuMjQoJ2I4JykKYjQgPSc5NTovL2FiLmMzLjk2LzUyLzE0My9mNj8xNGU9JwpiNSA9JyZjZD0xM2UmMTMwPWVmJjE0YT0xMGQmMTM3PTNiJjU4PTc3JmMyPTUwJwoKCjE0OCA2NCgpOgoJMTNhPTRhKDlkKQkKCTIzPTM2LjI2KCdlND0iKC4rPykiLis/NDY9IiguKz8pIi4rP2ZjPSIoLis/KSInLDM2LjY3KS4yNSgxM2EpCgk0NCBlNCw0Niw2MyAzMiAyMzoKCQkxYiAxMzMgJ2QwJyAzMiBlNDoKCQkJMzQoZTQsNDYsMSw2Myw2KQoJCTFiICdkMCcgMzIgZTQ6CgkJCTFiIDY4ID09ICc4OCc6CgkJCQkxYiAzMCA9PSAnJzoKCQkJCSAgICA2NSA9IDEyLmE4KCkKCQkJCSAgICBhOSA9IDY1LmJjKCdjMCBhMycsICcxMzQgMTI2IDEwZiAxMDEgMTI0IGJmIDU5JywnJywnYWEgZjcgYSA0OSAxMDEgZWUgYzYgZmYnLCdhZicsJzEyZCAxNDUnKQoJCQkJICAgIDFiIGE5ID09IDE6CgkJCQkJNDggPSAxOS45MCgnJywgJzEwNCA4OScpCgkJCQkJNDguYTYoKQoJCQkJCTFiICg0OC42ZSgpKToKCQkJCQkgICAgNzMgPSA0OC45ZSgpCgkJCQkJICAgIDE0LmJlKCc0OScsNzMpICAgICAgCgkJCQkJMzQoZTQsNDYsMSw2Myw2KQoJCQkxYiA2OCA9PSAnODgnOgoJCQkJMWIgMzAgPD4gJyc6CgkJCQkJMzQoZTQsNDYsMSw2Myw2KQoJNDIoJzE0MSAxMmUgZjEgMTJiJywnNDYnLDIsJ2RmOi8vYWIuNmQuMTIyL2E3LzEwYS9mMi4xMzknLDYpCgkxOS5mKCcyZS4yMCgxMzUpJykKICAgICAgCjE0OCA2YSg0Nik6CgkxYiAnNjQnIDMyIDQ2OgoJCThkKDQ2KQoJMWIgJ2QwJyAzMiA0NjoKCQkxYiAzMCA8PiAnJzoKCQkJNjUgPSAxMi5hOCgpCgkJCWE5ID0gNjUuYmMoJ2MwIGEzJywgJ2FhIDExMiAxMDMgNDkgMTMxIGY3JywnMTAxIGQ2JywnJywnYWYnLCcxMjAgMTQ2IDEwMyAxMGInKQoJCQkxYiBhOSA9PSAxOgoJCQkgICA0YzogICAgIAoJCQkgICAgICA0OCA9IDE5LjkwKCcnLCAnMTA0IDg5JykKCQkJICAgICAgNDguYTYoKQoJCQkgICAgICAxYiAoNDguNmUoKSk6CgkJCQkgICAgNzMgPSA0OC45ZSgpCgkJCSAgICAgIDFiIDczID09IDMwOgoJCQkJMWYgPSA1NSg0NikKCQkJCTQ0IDdjIDMyIDFmOgoJCQkJICAgICAgIDQyKDdjWyJlNCJdLDdjWyI0NiJdLDMsNjMsNikKCQkJICAgMTg6M2MKCTFiICdiMCcgMzIgNDY6CgkJMWYgPSA1NSg0NikKCQlmOSA9IDVkKDFmKQoJCTQ0IDdjIDMyIDFmOgoJCQk2Yyg3Y1siZTQiXSw3Y1siNDYiXSwzLDYzLGY5LDEzPTRmKQoJCWEyKCdiMCcsICcxMWEnKQoJCTFiICc2NCcgMzIgNDY6CgkJCTE5LmYoJzJlLjIwKDUwKScpCgk1MzoKCQkxMjUgPSA0NgoJCTFmID0gNTUoNDYpCgkJNDQgN2MgMzIgMWY6CgkJCTFiICc1Mi45Ni85YT80MD0nIDMyIDdjWyI0NiJdOgoJCQkJMzQoN2NbImU0Il0sN2NbIjQ2Il0sMyw2Myw2KQoJCQk1MzoKCQkJCTFiICdkNCcgMzIgN2NbIjQ2Il06CgkJCQkJMzQoN2NbImU0Il0sN2NbIjQ2Il0sMyw2Myw2KQoJCQkJNTM6CgkJCQkJNDIoN2NbImU0Il0sN2NbIjQ2Il0sMyw2Myw2KQoJCTE5LmYoJzJlLjIwKDUwKScpCgkKMTQ4IDhkKDQ2KToKCTEzYT00YSg0NikJCgkyMz0zNi4yNignZTQ9IiguKz8pIi4rPzQ2PSIoLis/KSIuKz9mYz0iKC4rPykiJywzNi42NykuMjUoMTNhKQoJNDQgZTQsNDYsNjMgMzIgMjM6CgkJMzQoZTQsNDYsMSw2Myw2KQoJMTkuZignMmUuMjAoNTApJykKCjE0OCA1NSg0Nik6CgkxM2E9NGEoNDYpCQoJNWE9MzYuMjYoJ14jLis/Oi0/WzAtOV0qKC4qPyksKC4qPylcMTAyKC4qPykkJywzNi4xNDQrMzYuMTQyKzM2LmZlKzM2LjE0OSkuMjUoMTNhKQoJZmQgPSBbXQoJNDQgNywgZTQsIDQ2IDMyIDVhOgoJCTJmID0geyI3IjogNywgImU0IjogZTQsICI0NiI6IDQ2fQoJCWZkLjgzKDJmKQoJYjMgPSBbXQoJNDQgN2MgMzIgZmQ6CgkJMmYgPSB7ImU0IjogN2NbImU0Il0sICI0NiI6IDdjWyI0NiJdfQoJCTVhPTM2LjI2KCcgKC4rPyk9IiguKz8pIicsMzYuMTQ0KzM2LjE0MiszNi5mZSszNi4xNDkpLjI1KDdjWyI3Il0pCgkJNDQgY2MsIGM0IDMyIDVhOgoJCQkyZltjYy5jMSgpLjExNygpLmNmKCctJywgJzE0ZicpXSA9IGM0LmMxKCkKCQliMy44MygyZikKCTFjIGIzCgkgICAgIAoxNDggOTEoNDYsZTQpOgoJICAgIDFiICdkNCcgMzIgNDY6CgkJICAgIDZhKDQ2KQoJICAgIDUzOgoJCSAgICAxYiAnNTIuOTYvOWE/NDA9JyAzMiA0NjoKCQkJNzUgPSA0Ni45NCgnNDA9JylbMV0KCQkJYzkgPSBiNCArIDc1ICsgYjUKCQkJM2QgPSAxNi41NChjOSkKCQkJM2QuMzgoJzhhLTcwJywgJzU2LzUuMCAoMWU7IGZlOyAxZSBkYiA1LjE7IGRhLWU3OyBlYToxLjkuMC4zKSA3NC8zNSA1Ny8zLjAuMycpCgkJCTE0ZCA9IDE2LjViKDNkKQoJCQkxM2E9MTRkLjhjKCkKCQkJMTRkLjcyKCkKCQkJMTNhID0gMTNhLmNmKCdcMTNkJywnJykuY2YoJ1wxMDInLCcnKS5jZignICAnLCcnKQoJCQkyMz0zNi4yNignImYwIjogIiguKz8pIi4rPyI5MiI6ICIoLis/KSInLDM2LjY3KS4yNSgxM2EpCgkJCTQ0IGUyLGU0IDMyIDIzOgoJCQkJNDYgPSAnOTU6Ly9hYi41Mi45Ni8xMGU/MTRiPScrZTIKCQkJCTQyKGU0LDQ2LDMsNjMsNikKCQkgICAgOGYgJ2JhJyAzMiA0NjoKCQkJICAgIDQ2ID0gNDYuY2YoJzc3JywnMTBjLzc3JykKCQkJICAgIDNkID0gMTYuNTQoNDYpCgkJCSAgICAzZC4zOCgnOGEtNzAnLCAnNTYvNS4wICgxZTsgZmU7IDFlIGRiIDUuMTsgZGEtZTc7IGVhOjEuOS4wLjMpIDc0LzM1IDU3LzMuMC4zJykKCQkJICAgIDE0ZCA9IDE2LjViKDNkKQoJCQkgICAgMTNhPTE0ZC44YygpCgkJCSAgICAxNGQuNzIoKQoJCQkgICAgMjM9MzYuMjYoJzEzYyIsIjQ2Ilw6IiguKz8pIicpLjI1KDEzYSlbMF0KCQkJICAgIDEzZj0yMy5jZignXC8nLCcvJykKCQkJICAgIDNmPTRiCgkJCSAgICAxMT0xMi4yYyhlNCwgMjI9NjMsZT02Myk7IDExLjMzKCA1OD0iY2IiLCAxZD17ICI2MiI6IGU0IH0gKQoJCQkgICAgM2Y9MTJjLjExOCgzZT01ZSgyYS4xYVsxXSksNDY9MTNmLDI5PTExKQoJCQkgICAgNGM6CgkJCQkgMTkuYWUgKCkuZDcoMTNmLCAxMSwgNGYpCgkJCQkgMWMgM2YKCQkJICAgIDE4OgoJCQkJIDNjCgkJICAgIDUzOgoJCQkxYiA0NS40ZCg0NikuZDUoKToKCQkJCTEzZiA9IDQ1LjRkKDQ2KS5mMygpCgkJCTUzOiAxM2Y9NDYgCgkJCTNmPTRiCgkJCTExPTEyLjJjKGU0LCAyMj02MyxlPTYzKTsgMTEuMzMoIDU4PSJjYiIsIDFkPXsgIjYyIjogZTQgfSApCgkJCTNmPTEyYy4xMTgoM2U9NWUoMmEuMWFbMV0pLDQ2PTEzZiwyOT0xMSkKCQkJNGM6CgkJCSAgICAgMTkuYWUgKCkuZDcoMTNmLCAxMSwgNGYpCgkJCSAgICAgMWMgM2YKCQkJMTg6CgkJCSAgICAgM2MKCSAgICAKMTQ4IDk5KCk6Cgk2OSA9ICcnCgllMCA9ICc5NTovL2Y4LmY1Ljk2LzEwNy8xNDcvNDMtNzgvMTJhPzg3JwoJM2QgPSAxNi41NChlMCkKCTNkLjM4KCc4YS03MCcsICc1Ni81LjAgKDFlOyBmZTsgMWUgZGIgNS4xOyBkYS1lNzsgZWE6MS45LjAuMykgNzQvMzUgNTcvMy4wLjMnKQoJMTRkID0gMTYuNWIoM2QpCgkxM2E9MTRkLjhjKCkKCTE0ZC43MigpCgkxM2EgPSAxM2EuY2YoJy8xMDInLCcnKQoJMTNhID0gMTNhLjgwKCdjZS04JykuZmEoJ2NlLTgnKS5jZignJiMzOTsnLCdcJycpLmNmKCcmIzEwOycsJyAtICcpLmNmKCcmIzExMzsnLCcnKQoJMjM9MzYuMjYoIjw5Mj4oLis/KTwvOTI+Lis/PGExPiguKz8pPC9hMT4iLDM2LjY3KS4yNSgxM2EpWzE6XQoJNDQgMjgsIDdlIDMyIDIzOgoJICAgIDRjOgoJCQkgICAgMjggPSAyOC44MCgnMTE0JywgJ2IyJykKCSAgICAxODoKCQkJICAgIDI4ID0gMjguODAoJ2NlLTgnLCdiMicpCgkgICAgN2UgPSA3ZVs6LTE1XQoJICAgIDI4ID0gMjguY2YoJyYxM2I7JywnJykKCSAgICA3ZSA9ICdbNzYgZDhdW2JdJys3ZSsnWy9iXVsvNzZdJwoJICAgIDY5ID0gNjkrN2UrJ1wxMDInKzI4KydcMTAyJysnXDEwMicKCThlKCdbNzYgZDhdW2JdQGVkWy9iXVsvNzZdJywgNjkpCgoxNDggOGUoYTUsIDY5KToKICAgIGU1ID0gMTExCiAgICAxOS5mKCc5YiglZCknICUgZTUpCiAgICAxOS5jOCgxMDApCiAgICBkMyA9IDEyLmZiKGU1KQogICAgOTMgPSA1MAogICAgMTE1ICg5MyA+IDApOgoJNGM6CgkgICAgMTkuYzgoMTApCgkgICAgOTMgLT0gMQoJICAgIGQzLjcxKDEpLmQ5KGE1KQoJICAgIGQzLjcxKDUpLmVjKDY5KQoJICAgIDFjCgkxODoKCSAgICAzYwoJCQkJICAgICAKMTQ4IDRhKDQ2KToKCTQ2ICs9ICc/JWQ9JWQnICUgKDg0LjljKDEsIGJiKSwgODQuOWMoMSwgYmIpKQoJM2QgPSAxNi41NCg0NikKCTNkLjM4KCc4YS03MCcsICc1Ni81LjAgKDFlOyBmZTsgMWUgZGIgNS4xOyBkYS1lNzsgZWE6MS45LjAuMykgNzQvMzUgNTcvMy4wLjMnKQoJMTRkID0gMTYuNWIoM2QpCgkxM2E9MTRkLjhjKCkKCTEzYSA9IDEzYS5jZignXDEzZCcsJycpLmNmKCdcMTRjJywnJykuY2YoJyYxMWU7JywnJykuY2YoJ1wnJywnJykKCTE0ZC43MigpCgkxYyAxM2EKCjE0OCA3YSgpOgoJNmY9W10KCTZiPTJhLjFhWzJdCgkxYiA1ZCg2Yik+PTI6CgkJNz0yYS4xYVsyXQoJCTVmPTcuY2YoJz8nLCcnKQoJCTFiICg3WzVkKDcpLTFdPT0nLycpOgoJCQk3PTdbMDo1ZCg3KS0yXQoJCTNhPTVmLjk0KCcmJykKCQk2Zj17fQoJCTQ0IDE0MCAzMiAxMTAoNWQoM2EpKToKCQkJMjE9e30KCQkJMjE9M2FbMTQwXS45NCgnPScpCgkJCTFiICg1ZCgyMSkpPT0yOgoJCQkJNmZbMjFbMF1dPTIxWzFdCgkJCSAgICAgICAKCTFjIDZmCgkgICAgICAgCjE0OCAzNChlNCw0NiwxMWMsNjMsNixjPScnKToKCWUzPTJhLjFhWzBdKyI/NDY9IisxMzIuNCg0NikrIiYxMWM9Iis1MSgxMWMpKyImZTQ9IisxMzIuNChlNCkrIiY2Mz0iKzEzMi40KDYzKSsiJmM9IisxMzIuNChjKQoJM2Y9NGIKCTExPTEyLjJjKGU0LCAyMj0iNjEuZDIiLCBlPTYzKQoJMTEuMzMoIDU4PSJjYiIsIDFkPXsgIjYyIjogZTQsICdlYic6IGMgfSApCgkxMS4zMSgnMmQnLCA2KQoJM2Y9MTJjLjExOCgzZT01ZSgyYS4xYVsxXSksNDY9ZTMsMjk9MTEsMTM9NGIpCgkxYyAzZgoKMTQ4IDQyKGU0LDQ2LDExYyw2Myw2LGM9JycpOgoJZTM9MmEuMWFbMF0rIj80Nj0iKzEzMi40KDQ2KSsiJjExYz0iKzUxKDExYykrIiZlND0iKzEzMi40KGU0KSsiJjYzPSIrMTMyLjQoNjMpKyImYz0iKzEzMi40KGMpCgkzZj00YgoJMTE9MTIuMmMoZTQsIDIyPSI2MS5kMiIsIGU9NjMpCgkxMS4zMyggNTg9ImNiIiwgMWQ9eyAiNjIiOiBlNCwgJ2ViJzogYyB9ICkKCTExLjMxKCcyZCcsIDYpCgkzZj0xMmMuMTE4KDNlPTVlKDJhLjFhWzFdKSw0Nj1lMywyOT0xMSwxMz00ZikKCTFjIDNmCgoxNDggNmMoZTQsNDYsMTFjLDYzLDgyLDEzPTRmKToKCTFiIGE0PT0nODgnOgoJICAgIDQxPWU0Ljg1KCcoJykKCSAgICA0ZT0iIgoJICAgIDE3PSIiCgkgICAgMWIgNWQoNDEpPjA6CgkJNGU9NDFbMF0KCQkxNz00MVsyXS44NSgnKScpCgkgICAgMWIgNWQoMTcpPjA6CgkJMTc9MTdbMF0KCSAgICA3OSA9IDk4LmRjKCcxMTknLCA0ZSAsMTcpCgkgICAgZTM9MmEuMWFbMF0rIj80Nj0iKzEzMi40KDQ2KSsiJjQ3PSIrNTEoNDcpKyImMTFjPSIrNTEoMTFjKSsiJmU0PSIrMTMyLjQoZTQpCgkgICAgM2Y9NGIKCSAgICAxMT0xMi4yYyhlNCwgMjI9NzlbJzg2J10sIGU9NzlbJzg2J10pCgkgICAgMTEuMzMoIDU4PSJjYiIsIDFkPSA3OSApCgkgICAgMmIgPSBbXQoJICAgIDJiLjgzKCgnMTE2IGI3JywgJzEyOS4xMDUoMTFmKScpKQoJICAgIDExLjdkKDJiLCBiMT00YikKCSAgICAxMS4zMSgnMmQnLCA3OVsnYWMnXSkKCSAgICAzZj0xMmMuMTE4KDNlPTVlKDJhLjFhWzFdKSw0Nj1lMywyOT0xMSwxMz0xMyxjNz04MikKCSAgICAxYyAzZgoJNTM6CgkgICAgZTM9MmEuMWFbMF0rIj80Nj0iKzEzMi40KDQ2KSsiJjQ3PSIrNTEoNDcpKyImMTFjPSIrNTEoMTFjKSsiJmU0PSIrMTMyLjQoZTQpCgkgICAgM2Y9NGIKCSAgICAxMT0xMi4yYyhlNCwgMjI9NjMsIGU9NjMpCgkgICAgMTEuMzMoIDU4PSJjYiIsIDFkPXsgIjYyIjogZTQgfSApCgkgICAgMTEuMzEoJzJkJywgNikKCSAgICAzZj0xMmMuMTE4KDNlPTVlKDJhLjFhWzFdKSw0Nj1lMywyOT0xMSwxMz0xMykKCSAgICAxYyAzZgoJCjE0OCBhMig1OSwgOGIpOgogICAgMWIgNTk6CgkxMmMuYzUoNWUoMmEuMWFbMV0pLCA1OSkKICAgIDFiIDE0LjI0KCcxMWQtMTI4Jyk9PSc4OCc6CgkxOS5mKCIyZS4yMCglMTQ3KSIgJSAxNC4yNCg4YikgKQoKNz03YSgpOyA0Nj01YzsgZTQ9NWM7IDExYz01YzsgNDc9NWM7IDYzPTVjCjRjOiA0Nz0xMzIuMjcoN1siNDciXSkKMTg6IDNjCjRjOiA0Nj0xMzIuMjcoN1siNDYiXSkKMTg6IDNjCjRjOiBlND0xMzIuMjcoN1siZTQiXSkKMTg6IDNjCjRjOiAxMWM9NWUoN1siMTFjIl0pCjE4OiAzYwo0YzogNjM9MTMyLjI3KDdbIjYzIl0pCjE4OiAzYwogCiM3YiAiMTJmOiAiKzUxKDQ3KTsgN2IgIjEyNzogIis1MSgxMWMpOyA3YiAiMTM4OiAiKzUxKDQ2KTsgN2IgIjEyMTogIis1MShlNCkKIAoxYiAxMWM9PTVjIDExYiA0Nj09NWMgMTFiIDVkKDQ2KTwxOiA2NCgpCjhmIDExYz09MTo2YSg0NikKOGYgMTFjPT0yOjk5KCkKOGYgMTFjPT0zOjkxKDQ2LGU0KQoKMTJjLmEwKDVlKDJhLjFhWzFdKSk=")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|2|3|quote_plus|5|fanart|params|8|9|a|B|description|d|thumbnailImage|executebuiltin|10|liz|xbmcgui|isFolder|selfAddon|15|urllib2|simpleyear|except|xbmc|argv|if|return|infoLabels|Windows|channels|SetViewMode|splitparams|iconImage|match|getSetting|findall|compile|unquote_plus|status|listitem|sys|contextMenuItems|ListItem|fanart_image|Container|item_data|adultpass|setProperty|in|setInfo|addDir|2008092417|re|addon_id|add_header|39|pairsofparams|AIzaSyA7v1QOHz8Q4my5J8uGSpr0zRrntRjnMmk|pass|req|handle|ok|search_query|splitName|addLink|AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_|for|urlresolver|url|site|keyb|password|open_url|True|try|HostedMediaFile|simplename|False|50|str|youtube|else|Request|GetList|Mozilla|Firefox|type|content|matches|urlopen|None|len|int|cleanedparams|translatePath|DefaultFolder|Title|iconimage|Index|dialog|metahandlers|DOTALL|adultopt|text|GetChans|paramstring|addLinkMeta|metalkettle|isConfirmed|param|Agent|getControl|close|passw|Gecko|searchterm|COLOR|video|b7Up8kQt11xgVwz3ErTo|meta|get_params|print|channel|addContextMenuItems|dte|xbmcaddon|decode|import|itemcount|append|random|partition|cover_url|588677963413065728|true|Password|User|viewType|read|CatIndex|showText|elif|Keyboard|PLAYLINK|title|retry|split|https|com|Addon|metaget|TWITTER|results|ActivateWindow|randint|baseurl|getText|special|endOfDirectory|pubDate|setView|Content|metaset|heading|doModal|UKTurk|Dialog|ret|Please|www|backdrop_url|addons|Player|Cancel|movies|replaceItems|ignore|list|ytapi1|ytapi2|common_addon|Information|enable_meta|metahandler|dailymotion|10000|yesno|preparezip|setSetting|adult|Adult|strip|maxResults|googleapis|value|setContent|accidental|totalItems|sleep|ytapi|addon|Video|field|regionCode|utf|replace|XXX|resources|png|win|txt|valid_url|continue|play|blue|setLabel|en|NT|get_meta|from|join|http|twit|icon|ytid|u|name|id|MetaData|GB|home|path|rv|plot|setText|uk_turk|prevent|snippet|videoId|Twitter|twitter|resolve|queries|google|search|set|script|cnt|encode|Window|img|li|U|access|100|to|n|the|Set|Action|os|macros|ukturk|plugin|thumbs|money|embed|en_US|watch|opted|range|10147|enter|x2026|ascii|while|Movie|lower|addDirectoryItem|movie|MAIN|or|mode|auto|nbsp|Info|Show|Name|co|libs|show|burl|have|Mode|view|XBMC|exec|Feed|xbmcplugin|Lets|Turk|Site|part|you|urllib|not|You|500|get|key|URL|jpg|link|amp|mp4|r|US|streamurl|i|UK|M|v3|I|Go|me|s|def|S|hl|v|t|response|q|_".split("|")))