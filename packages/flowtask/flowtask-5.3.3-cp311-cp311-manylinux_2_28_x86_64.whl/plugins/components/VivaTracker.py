from flowtask.components import UserComponent


class VivaTracker(UserComponent):

    async def start(self, **kwargs):
        print('Starting VivaTracker')
        print(f'Account is : {self.account}')
        return True

    async def run(self):
        print('Running VivaTracker')
        return True

    async def close(self):
        print('Closing VivaTracker')
        return True
