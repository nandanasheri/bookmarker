CREATE TABLE bookmarks (
  id SERIAL PRIMARY KEY,
  url VARCHAR (500) NOT NULL,
  title VARCHAR (500) NOT NULL,
  notes VARCHAR (500),
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR (20) NOT NULL
);

CREATE TABLE bookmarked (
  bookmark_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (bookmark_id, tag_id),
  FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
