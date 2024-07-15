import pytest

from chatbot.dependencies.TitleGenerator import TitleGenerator
from dotenv import load_dotenv

load_dotenv(override=True)
title_generator = TitleGenerator()


def test_title_generator_instance_singleton():
    instance2 = TitleGenerator()

    assert id(title_generator) == id(instance2)


@pytest.mark.asyncio(scope="session")
async def test_generate_title():
    message = """
    It was 7 minutes after midnight. The dog was lying on the grass in the middle of the lawn in front of Mrs Shears’ house. Its eyes were closed. It looked as if it was running on its side, the way dogs run when they think they are chasing a cat in a dream. But the dog was not running or asleep. The dog was dead. There was a garden fork sticking out of the dog. The points of the fork must have gone all the way through the dog and into the ground because the fork had not fallen over. I decided that the dog was probably killed with the fork because I could not see any other wounds in the dog and I do not think you would stick a garden fork into a dog after it had died for some other reason, like cancer for example, or a road accident. But I could not be certain about this.

I went through Mrs Shears’ gate, closing it behind me. I walked onto her lawn and knelt beside the dog. I put my hand on the muzzle of the dog. It was still warm.

The dog was called Wellington. It belonged to Mrs Shears who was our friend. She lived on the opposite side of the road, two houses to the left.
    """

    response = await title_generator.generate_title(message)

    print(response)

    assert response
