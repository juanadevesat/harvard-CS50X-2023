SELECT AVG(songs.energy) FROM songs JOIN artists ON artist_id = artists.id WHERE artists.name = 'Drake';