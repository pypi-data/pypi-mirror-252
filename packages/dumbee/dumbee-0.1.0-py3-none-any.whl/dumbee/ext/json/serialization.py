import json
import dumbee
import re


class Serializer(dumbee.Middleware):
    @property
    def paths(self) -> list:
        """
        Returns list of paths on which to execute this middleware

        Returns
        -------
        list
        """
        return self.params.get("paths", ["."])

    @property
    def encoder(self) -> json.JSONEncoder:
        """
        Return the JSON encoder
        """
        return self.params.get("serializer", json.JSONEncoder)

    @property
    def decoder(self) -> json.JSONDecoder:
        """
        Return the JSON decoder
        """
        return self.params.get("deserializer", json.JSONDecoder)

    def __call__(self, query, next: callable):
        """
        Apply the middleware a query
        """
        if self.handles(query):
            return dumbee.Pipeline([self.encode, self.decode])(query, next)
        return next(query)

    def handles(self, query) -> bool:
        """
        Return True if the query path matches any
        parametrized path
        """
        for path in self.paths:
            if re.match(path, query.path):
                return True
        return False

    def encode(self, query, next: callable):
        """
        Serialize content
        """
        if query.type == "write":
            return next(
                query.replace(
                    content=json.dumps(
                        query.content,
                        indent=self.params.get("indent", 4),
                        cls=self.encoder,
                    )
                )
            )

        return next(query)

    def decode(self, query, next: callable):
        """
        Deserialize content
        """
        if query.type == "read":
            return json.loads(next(query), cls=self.decoder)
        return next(query)
