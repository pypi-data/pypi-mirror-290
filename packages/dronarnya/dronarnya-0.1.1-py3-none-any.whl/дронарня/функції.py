from .класи import ТрЗасіб, ПерелікМов, повідомити
# Україномовні команди
from пітон.ядро import *
from пітон.ядро.типи_данних import *

import logging

def default_still_waiting_callback(atts):
    logging.getLogger(__name__).debug("Still waiting for data from vehicle: %s" % ','.join(atts))


def підєднати(сз: строка = Жоден,
            _ініціалізовувати: логічне = Істина,
            чекати_готовність: (логічне, Жоден) = Жоден,
            мова = Жоден,
            timeout=30,
            still_waiting_callback=default_still_waiting_callback,
            still_waiting_interval=1,
            клас_транспорту: (ТрЗасіб, Жоден) = Жоден,
            частота=4,
            швидкість=115200,
            heartbeat_timeout=30,
            source_system=255,
            source_component=0,
            use_native=Хиба):
    """
    Returns a :py:class:`Vehicle` object connected to the address specified by string parameter ``ip``.
    Connection string parameters (``ip``) for different targets are listed in the :ref:`getting started guide <get_started_connecting>`.

    The method is usually called with ``wait_ready=True`` to ensure that vehicle parameters and (most) attributes are
    available when ``connect()`` returns.

    .. code:: python

        from dronekit import connect

        # Connect to the Vehicle using "connection string" (in this case an address on network)
        vehicle = connect('127.0.0.1:14550', wait_ready=True)

    :param Строка сз: Строка з'єднання <get_started_connecting> до ціьової адреси - наприклад 127.0.0.1:14550.
    :param тип_тз: Тип транспортного засобу 
    :param тип_прошивки: Тип прошивки контролера керування

    :param (логічне,список) чекати_готовність: якщо `Істина` чекаемо на повернення всіх необхідних атрибутів
        (за замовчанням `Жодне`).
        Необхідні атрибути: :py:attr:`parameters`, :py:attr:`gps_0`, :py:attr:`armed`, :py:attr:`mode`, and :py:attr:`attitude`.

        Такожи можливо вказати у списку параметри яких функції необхідно чекати (наприклад ``чекати_готовність=['system_status','mode']``).

        Більше інформації дивитися тут:  :py:func:`ТрЗасіб.wait_ready <Vehicle.wait_ready>`.

    :param Vehicle vehicle_class: The class that will be instantiated by the ``connect()`` method.
        This can be any sub-class of ``Vehicle`` (and defaults to ``Vehicle``).
    :param число частота: Частота оновлення потоку данних від контроллера вказана у герцах. Значення за замовчанням 4Гц (4 блоків данних на секунду).
    :param число швидкість: Швидкість передачі данні у з'єднанні. За замовчанням 115200.
    :param int heartbeat_timeout: Connection timeout value in seconds (default is 30s).
        If a heartbeat is not detected within this time an exception will be raised.
    :param int source_system: The MAVLink ID of the :py:class:`Vehicle` object returned by this method (by default 255).
    :param int source_component: The MAVLink Component ID fo the :py:class:`Vehicle` object returned by this method (by default 0).
    :param bool use_native: Use precompiled MAVLink parser.

        .. note::

            The returned :py:class:`Vehicle` object acts as a ground control station from the
            perspective of the connected "real" vehicle. It will process/receive messages from the real vehicle
            if they are addressed to this ``source_system`` id. Messages sent to the real vehicle are
            automatically updated to use the vehicle's ``target_system`` id.

            It is *good practice* to assign a unique id for every system on the MAVLink network.
            It is possible to configure the autopilot to only respond to guided-mode commands from a specified GCS ID.

            The ``status_printer`` argument is deprecated. To redirect the logging from the library and from the
            autopilot, configure the ``dronekit`` and ``autopilot`` loggers using the Python ``logging`` module.


    :returns: A connected vehicle of the type defined in ``vehicle_class`` (a superclass of :py:class:`Vehicle`).
    """

    from .mavlink import MAVConnection

    if not клас_транспорту:
        клас_транспорту = ТрЗасіб

    надрукувати(f">>Підєднуємося до дрону за адресою {сз}")

    handler = MAVConnection(сз, baud=швидкість, source_system=source_system, source_component=source_component,
                            use_native=use_native)

    if мова == Жоден:
        мова = ПерелікМов.УКР

    трзасіб = клас_транспорту(handler, мова=мова)

    if _ініціалізовувати:
        трзасіб.ініціалізація(частота=частота, тайм_аут_серцебиття=heartbeat_timeout)

    if чекати_готовність:
        if чекати_готовність is Істина:
            трзасіб.wait_ready(still_waiting_interval=still_waiting_interval,
                               still_waiting_callback=still_waiting_callback,
                               timeout=timeout)
    else:
        трзасіб.wait_ready(*чекати_готовність)

    повідомити(контекст=трзасіб,
        рівень=10,
        анг=f">>Connecting is successful in adress {сз}",
        укр=f">>Підключення виконано успішно за адресою {сз}")

    return трзасіб